"""Passo 1-bis (docs/judge_rubric/08): test di ammissione del giudice C1/C2.

Fa giudicare al giudice (di default quello di sistema, config.MODELS['judge'])
i report di calibrazione C1 (corretto, riscritto) e C2 (plausibile ma
sbagliato) salvati in docs/judge_rubric/calibration_c1c2/, K volte ciascuno.
Calcola il Calibration Gap CGP = mean(score C1) - mean(score C2) per task e
complessivo, e il tasso di promozione di C2 alle soglie 0.7 e 0.65.

Uso:
    python scripts/judge_calibration/run_c1c2.py [--model <m>] [--local] [-k 3]
Output:
    results/evaluation/judge_calibration/c1c2_<model>.md (+ .json)
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
from agents._llm_utils import resolve_model_config  # noqa: E402
from agents.judge_agent import run_judge_textual  # noqa: E402
from utils.experiment_utils import build_judge_prompt  # noqa: E402
from utils.task_utils import _extract_json_blocks, _model_slug  # noqa: E402

C1C2_DIR = Path("docs/judge_rubric/calibration_c1c2")
OUT_DIR = os.path.join(config.RESULTS_PATH, "evaluation", "judge_calibration")


def normalize_total(judge_score, rubric):
    total = judge_score.get("total_score")
    if total is None:
        total = sum(
            v for k, v in judge_score.items()
            if k.endswith("_score") and k != "total_score" and isinstance(v, (int, float))
        )
    total_max = rubric.get("total_max", 0)
    total = float(min(max(float(total), 0.0), float(total_max)) if total_max else float(total))
    return round(total / total_max, 3) if total_max else 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None,
                        help="default: giudice di sistema (config.MODELS['judge'])")
    parser.add_argument("--local", action="store_true")
    parser.add_argument("-k", type=int, default=3, help="ripetizioni per report")
    args = parser.parse_args()

    if args.model:
        model, is_hosted = args.model, not args.local
    else:
        model, is_hosted = resolve_model_config("judge")

    reports = sorted(C1C2_DIR.glob("task*_C[12].json"))
    if not reports:
        raise SystemExit(f"Nessun report C1/C2 in {C1C2_DIR} — generare prima i materiali")

    rows = []
    for report_path in reports:
        task_id, kind = report_path.stem.rsplit("_", 1)
        task_content = Path(f"docs/tasks/{task_id}.md").read_text(encoding="utf-8")
        blocks = _extract_json_blocks(Path(f"docs/tasks/{task_id}_sol.md").read_text(encoding="utf-8"))
        rubric = blocks[1] if len(blocks) > 1 else {}
        agent_response = json.loads(report_path.read_text(encoding="utf-8"))
        for k in range(1, args.k + 1):
            print(f"[{task_id} {kind} k={k}] judging with {model}...")
            score, _, _ = run_judge_textual(
                task_content=task_content,
                rubric=rubric,
                agent_response=agent_response,
                system_prompt=build_judge_prompt(rubric),
                model=model,
                temperature=config.TEMPERATURE,
                base_url=config.OLLAMA_BASE_URL,
                is_hosted=is_hosted,
            )
            rows.append({
                "task_id": task_id,
                "kind": kind,
                "k": k,
                "normalized_score": normalize_total(score, rubric),
                "scores": {key: v for key, v in score.items() if key.endswith("_score")},
                "feedback": score.get("feedback", ""),
            })

    slug = _model_slug(model, is_hosted)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, f"c1c2_{slug}.json"), "w") as f:
        json.dump(rows, f, indent=2)

    tasks = sorted(set(r["task_id"] for r in rows))

    def mean(vals):
        return sum(vals) / len(vals) if vals else float("nan")

    def scores_of(task, kind):
        return [r["normalized_score"] for r in rows if r["task_id"] == task and r["kind"] == kind]

    all_c1 = [r["normalized_score"] for r in rows if r["kind"] == "C1"]
    all_c2 = [r["normalized_score"] for r in rows if r["kind"] == "C2"]
    c2_pass_07 = sum(1 for s in all_c2 if s >= 0.7)
    c2_pass_065 = sum(1 for s in all_c2 if s >= 0.65)
    c1_fail_065 = sum(1 for s in all_c1 if s < 0.65)

    lines = [
        f"# Test di ammissione C1/C2 — giudice {model} (passo 1-bis, doc judge_rubric/08)",
        "",
        f"- Report giudicati: {len(reports)} × K={args.k} = {len(rows)} giudizi",
        f"- **CGP complessivo = {mean(all_c1) - mean(all_c2):+.3f}** "
        f"(C1 medio {mean(all_c1):.3f}, C2 medio {mean(all_c2):.3f})",
        f"- C2 promossi (falsi positivi del giudice): {c2_pass_07}/{len(all_c2)} a t=0.7 — "
        f"{c2_pass_065}/{len(all_c2)} a t=0.65",
        f"- C1 bocciati (falsi negativi del giudice): {c1_fail_065}/{len(all_c1)} a t=0.65",
        "",
        "| task | C1 medio (min–max) | C2 medio (min–max) | CGP |",
        "|---|---|---|---|",
    ]
    for t in tasks:
        c1, c2 = scores_of(t, "C1"), scores_of(t, "C2")
        lines.append(
            f"| {t} | {mean(c1):.2f} ({min(c1):.2f}–{max(c1):.2f}) | "
            f"{mean(c2):.2f} ({min(c2):.2f}–{max(c2):.2f}) | {mean(c1) - mean(c2):+.2f} |"
        )
    with open(os.path.join(OUT_DIR, f"c1c2_{slug}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
