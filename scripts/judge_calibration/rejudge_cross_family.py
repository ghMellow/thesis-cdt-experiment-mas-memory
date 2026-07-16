"""Passo 1b (docs/judge_rubric/08): ri-giudizio con giudice di famiglia diversa.

Rilegge i final_answer salvati in results/ e li fa rigiudicare a un modello
non-gemma con la stessa rubrica, lo stesso prompt (build_judge_prompt) e la
stessa temperatura del giudice di sistema: cambia solo il modello. Nessuna
run nuova degli agenti.

Uso:
    python scripts/judge_calibration/rejudge_cross_family.py [--model gpt-oss:20b] [--local]
Output:
    results/evaluation/judge_calibration/cross_family_<model>.md (+ .json)
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

import config  # noqa: E402
from agents.judge_agent import run_judge_textual  # noqa: E402
from utils.experiment_utils import build_judge_prompt  # noqa: E402
from utils.task_utils import _extract_json_blocks, _model_slug  # noqa: E402

OUT_DIR = os.path.join(config.RESULTS_PATH, "evaluation", "judge_calibration")


def load_rubric_and_task(task_path: str, sol_path: str):
    task_content = Path(task_path).read_text(encoding="utf-8")
    json_blocks = _extract_json_blocks(Path(sol_path).read_text(encoding="utf-8"))
    rubric = json_blocks[1] if len(json_blocks) > 1 else {}
    return task_content, rubric


def normalize(judge_score, rubric):
    """Same total/normalized computation as the in-loop judge node."""
    total = judge_score.get("total_score")
    if total is None:
        total = sum(
            v for k, v in judge_score.items()
            if k.endswith("_score") and k != "total_score" and isinstance(v, (int, float))
        )
    total_max = rubric.get("total_max", 0)
    total = float(min(max(float(total), 0.0), float(total_max)) if total_max else float(total))
    judge_score["total_score"] = total
    judge_score["normalized_score"] = round(total / total_max, 3) if total_max else 0.0
    return judge_score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-oss:20b")
    parser.add_argument("--local", action="store_true",
                        help="usa Ollama locale invece dell'API hosted")
    args = parser.parse_args()
    is_hosted = not args.local

    rows = []
    for path in sorted(glob.glob(os.path.join(config.RESULTS_PATH, "*", "*", "agent", "*.json"))):
        with open(path) as f:
            data = json.load(f)
        if data.get("task_type") != "textual":
            continue
        task_content, rubric = load_rubric_and_task(data["task_path"], data["sol_path"])
        for rep in data.get("repetitions", []):
            original = rep.get("judge_score") or {}
            if "normalized_score" not in original:
                continue
            print(f"[{data['task_id']} rep {rep['repetition']}] judging with {args.model}...")
            new_score, _, _ = run_judge_textual(
                task_content=task_content,
                rubric=rubric,
                agent_response=rep["final_answer"],
                system_prompt=build_judge_prompt(rubric),
                model=args.model,
                temperature=config.TEMPERATURE,
                base_url=config.OLLAMA_BASE_URL,
                is_hosted=is_hosted,
            )
            new_score = normalize(new_score, rubric)
            rows.append({
                "task_id": data["task_id"],
                "repetition": rep["repetition"],
                "original_model": data["judge_model"],
                "original_normalized": original["normalized_score"],
                "new_model": args.model,
                "new_normalized": new_score["normalized_score"],
                "new_scores": {k: v for k, v in new_score.items() if k.endswith("_score")},
                "new_feedback": new_score.get("feedback", ""),
                "delta": round(new_score["normalized_score"] - original["normalized_score"], 3),
            })

    if not rows:
        raise SystemExit("Nessuna ripetizione textual trovata in results/")

    slug = _model_slug(args.model, is_hosted)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, f"cross_family_{slug}.json"), "w") as f:
        json.dump(rows, f, indent=2)

    def verdicts(t):
        flips = sum(
            1 for r in rows
            if (r["original_normalized"] >= t) != (r["new_normalized"] >= t)
        )
        return flips

    mean_delta = sum(r["delta"] for r in rows) / len(rows)
    lines = [
        f"# Ri-giudizio cross-family — {args.model} (passo 1b, doc judge_rubric/08)",
        "",
        f"- Ripetizioni rigiudicate: **{len(rows)}**",
        f"- Giudice originale: {rows[0]['original_model']} — nuovo giudice: {args.model}",
        f"- Delta medio (nuovo − originale): **{mean_delta:+.3f}**",
        f"- Verdetti flippati a t=0.7: {verdicts(0.7)}/{len(rows)} — a t=0.65: "
        f"{verdicts(0.65)}/{len(rows)}",
        "",
        "| task | rep | orig. | nuovo | delta |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['task_id']} | {r['repetition']} | {r['original_normalized']:.2f} | "
            f"{r['new_normalized']:.2f} | {r['delta']:+.2f} |"
        )
    with open(os.path.join(OUT_DIR, f"cross_family_{slug}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
