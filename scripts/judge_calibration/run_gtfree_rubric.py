"""Doc judge_rubric/10 e 12: rubriche GT-free nel banco di prova del doc 08.

Giudica con una rubrica task-independent caricata da file (default: v1,
`gtfree/rubric_v1.json`) e aggiunge il criterio di coverage calcolato
deterministicamente (0-2, stile SGV G2). Due varianti di coverage:
    functions  (v1) funzioni Go citate / funzioni nel task (cap 6)
    surfaces   (v2, doc 12 par. 4) superfici a rischio citate / superfici nel
               task -- una superficie = funzione con parametro *gin.Context
               (handler HTTP con input esterno, middleware/config CORS)

Due set:
    --set c1c2    i 10 report di calibrazione (CGP GT-free vs baseline doc 09)
    --set saved   i 15 final_answer salvati (flip rate vs rubrica GT-derivata,
                  accordo con M1-strict)

Uso:
    python scripts/judge_calibration/run_gtfree_rubric.py --set c1c2 [-k 3] \
        [--rubric docs/judge_rubric/gtfree/rubric_v2_draft.json --coverage surfaces]
Output:
    results/evaluation/judge_calibration/<prefix>_<set>_<model>.md (+ .json)
    dove <prefix> = gtfree (v1) o gtfree_v<N> (rubrica vN, dal nome file)
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
# Risk surface (doc 12 par. 4): a function taking *gin.Context -- HTTP
# handlers with external input plus middleware/config (e.g. CORS headers).
GO_SURFACE_RE = re.compile(
    r"func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)\s*\([^)]*\*gin\.Context"
)

# Judge output requirement of rubric v2 (doc 12 par. 3): motivations for
# every criterion scored below its max, appended to the rubric prompt.
MOTIVATION_INSTRUCTION = (
    "\n\nAdditional output requirement: in the Feedback section, for every "
    "criterion you score below its maximum, list which findings fail the "
    "check and why (for presence claims: which signature is missing in the "
    "cited snippet; for absence claims: which code path is not shown). "
    "Before awarding a maximum score, actively look for at least one finding "
    "that would fail the check and state why none does."
)


def task_functions(task_id, mode="functions"):
    """Go functions in the task's code extract: all of them (v1 coverage) or
    only risk surfaces, i.e. *gin.Context functions (v2 coverage)."""
    text = Path(f"docs/tasks/{task_id}.md").read_text(encoding="utf-8")
    regex = GO_SURFACE_RE if mode == "surfaces" else GO_FUNC_RE
    return sorted(set(regex.findall(text)))


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


def judge_k(task_id, agent_response, rubric, model, is_hosted, k, motivations=False):
    """K samples with the GT-free rubric; returns (llm totals, feedback texts)."""
    task_content = Path(f"docs/tasks/{task_id}.md").read_text(encoding="utf-8")
    system_prompt = build_judge_prompt(rubric)
    if motivations:
        system_prompt += MOTIVATION_INSTRUCTION
    totals, feedbacks = [], []
    for i in range(1, k + 1):
        print(f"[{task_id} k={i}] judging with {model} (GT-free rubric)...")
        score, _, _ = run_judge_textual(
            task_content=task_content,
            rubric=rubric,
            agent_response=agent_response,
            system_prompt=system_prompt,
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
        if motivations and score.get("feedback"):
            feedbacks.append(str(score["feedback"]))
    return totals, feedbacks


def combined(llm_totals, cov, rubric):
    """Mean combined normalized score: (mean LLM total + coverage) / (total_max + 2)."""
    mean_llm = sum(llm_totals) / len(llm_totals)
    denom = rubric["total_max"] + COVERAGE_MAX
    return round((mean_llm + cov) / denom, 3), round(min(llm_totals), 1), round(max(llm_totals), 1)


def report_text_of(response):
    return f"{response.get('answer', '')}\n{response.get('reasoning', '')}"


def run_c1c2(rubric, model, is_hosted, k, coverage_mode, motivations):
    rows = []
    for path in sorted(C1C2_DIR.glob("task*_C[12].json")):
        task_id, kind = path.stem.rsplit("_", 1)
        response = json.loads(path.read_text(encoding="utf-8"))
        funcs = task_functions(task_id, coverage_mode)
        cov, ratio, cited = coverage_score(report_text_of(response), funcs)
        totals, feedbacks = judge_k(
            task_id, response, rubric, model, is_hosted, k, motivations
        )
        norm, lo, hi = combined(totals, cov, rubric)
        rows.append({
            "task_id": task_id, "kind": kind, "llm_totals": totals,
            "coverage_score": cov, "coverage_ratio": ratio,
            "cited": cited, "n_exposed": len(funcs), "normalized_combined": norm,
            "llm_min": lo, "llm_max": hi, "judge_feedback": feedbacks,
        })
    return rows


def run_saved(rubric, model, is_hosted, k, coverage_mode, motivations):
    rows = []
    for path in sorted(glob.glob(os.path.join(config.RESULTS_PATH, "*", "*", "agent", "*.json"))):
        with open(path) as f:
            data = json.load(f)
        if data.get("task_type") != "textual":
            continue
        funcs = task_functions(data["task_id"], coverage_mode)
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
            totals, feedbacks = judge_k(
                data["task_id"], response, rubric, model, is_hosted, k, motivations
            )
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
                "m1_strict": m1_strict, "coverage_cited": cited,
                "judge_feedback": feedbacks,
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", choices=["c1c2", "saved"], required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--local", action="store_true")
    parser.add_argument("-k", type=int, default=3)
    parser.add_argument("--rubric", default=str(RUBRIC_PATH))
    parser.add_argument("--coverage", choices=["functions", "surfaces"],
                        default="functions")
    parser.add_argument("--motivations", action="store_true",
                        help="require per-criterion failure motivations (doc 12 par. 3)")
    args = parser.parse_args()

    rubric_path = Path(args.rubric)
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    ver_match = re.search(r"v(\d+)", rubric_path.stem)
    version = ver_match.group(1) if ver_match else "x"
    label = f"v{version}"
    prefix = "gtfree" if version == "1" else f"gtfree_v{version}"
    doc_ref = {"1": "10", "2": "12", "3": "14"}.get(version, "??")
    if args.model:
        model, is_hosted = args.model, not args.local
    else:
        model, is_hosted = resolve_model_config("judge")

    os.makedirs(OUT_DIR, exist_ok=True)
    slug = _model_slug(model, is_hosted)

    if args.set == "c1c2":
        rows = run_c1c2(rubric, model, is_hosted, args.k, args.coverage, args.motivations)
        c1 = [r["normalized_combined"] for r in rows if r["kind"] == "C1"]
        c2 = [r["normalized_combined"] for r in rows if r["kind"] == "C2"]
        cgp = sum(c1) / len(c1) - sum(c2) / len(c2)
        lines = [
            f"# Rubrica GT-free {label} — set C1/C2, giudice {model} "
            f"(doc judge_rubric/{doc_ref})",
            "",
            f"- **CGP GT-free = {cgp:+.3f}** (C1 medio {sum(c1) / len(c1):.3f}, "
            f"C2 medio {sum(c2) / len(c2):.3f}) — baseline GT-derivata (doc 09): +0.948",
            f"- C2 sopra soglia: {sum(1 for s in c2 if s >= 0.65)}/{len(c2)} a t=0.65 — "
            f"{sum(1 for s in c2 if s >= 0.7)}/{len(c2)} a t=0.7",
            f"- C1 sotto soglia a t=0.65: {sum(1 for s in c1 if s < 0.65)}/{len(c1)}",
            "",
            f"| task | kind | LLM medio/{rubric['total_max']} (min–max) | "
            f"coverage (ratio) | combinato /1 |",
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
        rows = run_saved(rubric, model, is_hosted, args.k, args.coverage, args.motivations)
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
            f"# Rubrica GT-free {label} — set report salvati, giudice {model} "
            f"(doc judge_rubric/{doc_ref})",
            "",
            f"- Ripetizioni: {len(rows)}",
            f"- Flip vs rubrica GT-derivata: {flips_065}/{len(rows)} a t=0.65 — "
            f"{flips_07}/{len(rows)} a t=0.7",
            f"- Accordo con M1-strict a t=0.65: {agree}/{len(defined)} "
            f"(baseline GT-derivata: 12/12)",
            "",
            f"| task | rep | GT-rubric | GT-free comb. | "
            f"LLM/{rubric['total_max']} (min–max) | cov | M1-strict |",
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

    with open(os.path.join(OUT_DIR, f"{prefix}_{args.set}_{slug}.json"), "w") as f:
        json.dump(rows, f, indent=2)
    with open(os.path.join(OUT_DIR, f"{prefix}_{args.set}_{slug}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
