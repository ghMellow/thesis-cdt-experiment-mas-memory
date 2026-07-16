"""Doc judge_rubric/10: rubrica GT-free (doc 05) nel banco di prova del doc 08.

Giudica con la rubrica task-independent `gtfree/rubric_v1.json` (3 criteri LLM,
total_max 7) e aggiunge il criterio di coverage calcolato deterministicamente
(0-2, stile SGV G2): funzioni Go esportate citate dal report / esposte nel
task. Score combinato normalizzato su 9.

Due set:
    --set c1c2    i 10 report di calibrazione (CGP GT-free vs baseline doc 09)
    --set saved   i 15 final_answer salvati (flip rate vs rubrica GT-derivata,
                  accordo con M1-strict)

Uso:
    python scripts/judge_calibration/run_gtfree_rubric.py --set c1c2 [-k 3]
Output:
    results/evaluation/judge_calibration/gtfree_<set>_<model>.md (+ .json)
"""

import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

import config  # noqa: E402
from agents._llm_utils import resolve_model_config  # noqa: E402
from agents.judge_agent import run_judge_textual  # noqa: E402
from utils.experiment_utils import build_judge_prompt  # noqa: E402
from utils.task_utils import _model_slug  # noqa: E402

RUBRIC_PATH = Path("docs/judge_rubric/gtfree/rubric_v1.json")
C1C2_DIR = Path("docs/judge_rubric/calibration_c1c2")
OUT_DIR = os.path.join(config.RESULTS_PATH, "evaluation", "judge_calibration")

COVERAGE_MAX = 2
# Effective denominator cap: on _full files with ~100 functions an absolute
# ratio would make full coverage unreachable for any honest report.
COVERAGE_DENOM_CAP = 6
GO_FUNC_RE = re.compile(r"func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)\s*\(")


def task_functions(task_id):
    """All Go functions (exported and not) in the task's code extract."""
    text = Path(f"docs/tasks/{task_id}.md").read_text(encoding="utf-8")
    return sorted(set(GO_FUNC_RE.findall(text)))


def coverage_score(report_text, functions):
    """Deterministic coverage: distinct task functions cited by the report,
    over min(n_functions, COVERAGE_DENOM_CAP). Ratio >= 2/3 -> 2,
    >= 1/3 -> 1, else 0 (declared in doc 10 par. 2)."""
    if not functions:
        return 0, 0.0, []
    cited = [f for f in functions if f in report_text]
    ratio = min(1.0, len(cited) / min(len(functions), COVERAGE_DENOM_CAP))
    score = 2 if ratio >= 2 / 3 else (1 if ratio >= 1 / 3 else 0)
    return score, round(ratio, 3), cited


def judge_k(task_id, agent_response, rubric, model, is_hosted, k):
    """K samples with the GT-free rubric; returns list of llm normalized-on-7 totals."""
    task_content = Path(f"docs/tasks/{task_id}.md").read_text(encoding="utf-8")
    totals = []
    for i in range(1, k + 1):
        print(f"[{task_id} k={i}] judging with {model} (GT-free rubric)...")
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
        total = score.get("total_score")
        if total is None:
            total = sum(
                v for key, v in score.items()
                if key.endswith("_score") and key != "total_score"
                and isinstance(v, (int, float))
            )
        total = min(max(float(total), 0.0), float(rubric["total_max"]))
        totals.append(total)
    return totals


def combined(llm_totals, cov, rubric):
    """Mean combined normalized score: (mean LLM total + coverage) / (7 + 2)."""
    mean_llm = sum(llm_totals) / len(llm_totals)
    denom = rubric["total_max"] + COVERAGE_MAX
    return round((mean_llm + cov) / denom, 3), round(min(llm_totals), 1), round(max(llm_totals), 1)


def report_text_of(response):
    return f"{response.get('answer', '')}\n{response.get('reasoning', '')}"


def run_c1c2(rubric, model, is_hosted, k):
    rows = []
    for path in sorted(C1C2_DIR.glob("task*_C[12].json")):
        task_id, kind = path.stem.rsplit("_", 1)
        response = json.loads(path.read_text(encoding="utf-8"))
        funcs = task_functions(task_id)
        cov, ratio, cited = coverage_score(report_text_of(response), funcs)
        totals = judge_k(task_id, response, rubric, model, is_hosted, k)
        norm, lo, hi = combined(totals, cov, rubric)
        rows.append({
            "task_id": task_id, "kind": kind, "llm_totals": totals,
            "coverage_score": cov, "coverage_ratio": ratio,
            "cited": cited, "n_exposed": len(funcs), "normalized_combined": norm,
            "llm_min": lo, "llm_max": hi,
        })
    return rows


def run_saved(rubric, model, is_hosted, k):
    rows = []
    for path in sorted(glob.glob(os.path.join(config.RESULTS_PATH, "*", "*", "agent", "*.json"))):
        with open(path) as f:
            data = json.load(f)
        if data.get("task_type") != "textual":
            continue
        funcs = task_functions(data["task_id"])
        for rep in data.get("repetitions", []):
            original = rep.get("judge_score") or {}
            if "normalized_score" not in original:
                continue
            response = rep["final_answer"]
            text = report_text_of(response)
            cvss = rep.get("history", [{}])[-1].get("cvss_estimate") or {}
            for finding in cvss.get("findings", []):
                text += "\n" + str(finding.get("function", ""))
            cov, ratio, cited = coverage_score(text, funcs)
            totals = judge_k(data["task_id"], response, rubric, model, is_hosted, k)
            norm, lo, hi = combined(totals, cov, rubric)
            cvss_eval = rep.get("cvss_eval") or {}
            m1_strict = (
                len(cvss_eval.get("missed_cves", [])) == 0
                if cvss_eval.get("n_target_cves", 0) > 0 else None
            )
            rows.append({
                "task_id": data["task_id"], "repetition": rep["repetition"],
                "gt_rubric_normalized": original["normalized_score"],
                "llm_totals": totals, "coverage_score": cov, "coverage_ratio": ratio,
                "normalized_combined": norm, "llm_min": lo, "llm_max": hi,
                "m1_strict": m1_strict,
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", choices=["c1c2", "saved"], required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--local", action="store_true")
    parser.add_argument("-k", type=int, default=3)
    args = parser.parse_args()

    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))
    if args.model:
        model, is_hosted = args.model, not args.local
    else:
        model, is_hosted = resolve_model_config("judge")

    os.makedirs(OUT_DIR, exist_ok=True)
    slug = _model_slug(model, is_hosted)

    if args.set == "c1c2":
        rows = run_c1c2(rubric, model, is_hosted, args.k)
        c1 = [r["normalized_combined"] for r in rows if r["kind"] == "C1"]
        c2 = [r["normalized_combined"] for r in rows if r["kind"] == "C2"]
        cgp = sum(c1) / len(c1) - sum(c2) / len(c2)
        lines = [
            f"# Rubrica GT-free v1 — set C1/C2, giudice {model} (doc judge_rubric/10)",
            "",
            f"- **CGP GT-free = {cgp:+.3f}** (C1 medio {sum(c1) / len(c1):.3f}, "
            f"C2 medio {sum(c2) / len(c2):.3f}) — baseline GT-derivata (doc 09): +0.948",
            f"- C2 sopra soglia: {sum(1 for s in c2 if s >= 0.65)}/{len(c2)} a t=0.65 — "
            f"{sum(1 for s in c2 if s >= 0.7)}/{len(c2)} a t=0.7",
            f"- C1 sotto soglia a t=0.65: {sum(1 for s in c1 if s < 0.65)}/{len(c1)}",
            "",
            "| task | kind | LLM medio/7 (min–max) | coverage (ratio) | combinato /1 |",
            "|---|---|---|---|---|",
        ]
        for r in rows:
            mean_llm = sum(r["llm_totals"]) / len(r["llm_totals"])
            lines.append(
                f"| {r['task_id']} | {r['kind']} | {mean_llm:.1f} "
                f"({r['llm_min']}–{r['llm_max']}) | {r['coverage_score']} "
                f"({r['coverage_ratio']}) | {r['normalized_combined']:.2f} |"
            )
    else:
        rows = run_saved(rubric, model, is_hosted, args.k)
        flips_065 = sum(
            1 for r in rows
            if (r["gt_rubric_normalized"] >= 0.65) != (r["normalized_combined"] >= 0.65)
        )
        flips_07 = sum(
            1 for r in rows
            if (r["gt_rubric_normalized"] >= 0.7) != (r["normalized_combined"] >= 0.7)
        )
        defined = [r for r in rows if r["m1_strict"] is not None]
        agree = sum(
            1 for r in defined if (r["normalized_combined"] >= 0.65) == r["m1_strict"]
        )
        lines = [
            f"# Rubrica GT-free v1 — set report salvati, giudice {model} (doc judge_rubric/10)",
            "",
            f"- Ripetizioni: {len(rows)}",
            f"- Flip vs rubrica GT-derivata: {flips_065}/{len(rows)} a t=0.65 — "
            f"{flips_07}/{len(rows)} a t=0.7",
            f"- Accordo con M1-strict a t=0.65: {agree}/{len(defined)} "
            f"(baseline GT-derivata: 12/12)",
            "",
            "| task | rep | GT-rubric | GT-free comb. | LLM/7 (min–max) | cov | M1-strict |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in rows:
            mean_llm = sum(r["llm_totals"]) / len(r["llm_totals"])
            m1s = "—" if r["m1_strict"] is None else ("✅" if r["m1_strict"] else "❌")
            lines.append(
                f"| {r['task_id']} | {r['repetition']} | {r['gt_rubric_normalized']:.2f} | "
                f"{r['normalized_combined']:.2f} | {mean_llm:.1f} "
                f"({r['llm_min']}–{r['llm_max']}) | {r['coverage_score']} | {m1s} |"
            )

    with open(os.path.join(OUT_DIR, f"gtfree_{args.set}_{slug}.json"), "w") as f:
        json.dump(rows, f, indent=2)
    with open(os.path.join(OUT_DIR, f"gtfree_{args.set}_{slug}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
