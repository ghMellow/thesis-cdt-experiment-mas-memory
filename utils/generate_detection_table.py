"""Reproduces Table "Detection Performance by NF and Configuration" for the paper.

Origin: the relatore rebuilt this table by hand from Lorenzo's summary counts
(call 2026-08-20, "l'ho creata... cercato di creare una storia che sembrasse
coerente, con i dati che avevo"), because at the time nobody could replicate
the numbers from the raw JSON. This script closes that gap: TP/FP/FN/Precision
are computed deterministically by reusing utils/cvss_eval.py's own matching
and aggregation functions (no reimplementation, no hand calculation) on the
raw repetitions saved under config.RESULTS_PATH. The Candidates column is the
one exception — it is inherently manual (expert review of unmatched findings,
docs/expert_review/03_CVE_CVSS_sast.md) and is cited here, not computed.

Canonical raw data per NF (documented so the choice is auditable, not
implicit — several NFs have more than one raw run on disk):

- PCF/AMF/UDM: experiment `1A` (no-hint) / `1A_sast_hint[_full]` (SAST-hint),
  3 repetitions each — the only run that exists for these three.
- UDR: experiment `1A` (no-hint, 3 reps) is the normal baseline run.
  `1A_sast_hint_full` on disk holds 10 repetitions — call 2026-08-20: "avevo
  fatto prima la run normale da tre... poi ne ho fatta un'altra da 10, ma
  isolata" (isolated re-run to check the SAST-hint finding wasn't noise, doc
  `docs/sgv_protocol/11_sast_hint_noise_test_2026-07-21.md`). Only the first
  3 repetitions are the run comparable to the other NFs; using all 10 would
  silently change the unit of analysis. Confirmed against the known-correct
  reference numbers in commit bd0dcc0 ("UDR SAST-hint: TP 9->3"): computing
  on reps[:3] reproduces TP=9 before the correction below, TP=3 after.

UDR spurious-match correction (bd0dcc0, 2026-08-05): the deterministic
function-name matcher pairs CVE-2026-40249 and CVE-2026-40343 to a finding
that always describes the deserialization-nil-pointer bug, never the CVEs'
actual root cause (missing return statement) — confirmed by reading every
repetition's narrative, flagged by Lorenzo in docs/expert_review/03. That
commit applied the fix only to a throwaway duplicate dataset to produce
docs/sgv_protocol/10b_/12b_ — never merged into the production ground truth,
which is why re-running the pipeline today still reproduces the pre-fix
numbers. This script applies the same fix, but as a persisted, documented
step (see `_corrected_dataset`) instead of a one-off untracked file, so the
table this script prints is the one to hand to the relatore, with a clear
answer to "how did you make this".

Usage:
    PYTHONPATH=. python utils/generate_detection_table.py [--paper-icai]
Output:
    Markdown + LaTeX table printed to stdout (not written to results/reports/
    — this is paper material, not a run report; copy it into
    docs/sgv_protocol/ by hand once reviewed).
"""

import argparse
import copy
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import config
from utils import cvss_eval

# CVEs whose deterministic handler-name match is spurious (bd0dcc0) — nulling
# handler_functions makes _match_finding() (utils/cvss_eval.py) skip them,
# same effect as removing them from the dataset without deleting the entry.
UDR_SPURIOUS_CVES = ["CVE-2026-40249", "CVE-2026-40343"]

NF_CONFIG: Dict[str, Dict[str, Any]] = {
    "PCF": {"task_id": "task5_vuln_pcf", "no_hint": "1A", "sast_hint": "1A_sast_hint", "sast_hint_max_reps": None},
    "UDR": {"task_id": "task6_vuln_udr_full", "no_hint": "1A", "sast_hint": "1A_sast_hint_full", "sast_hint_max_reps": 3},
    "AMF": {"task_id": "task7_vuln_amf_full", "no_hint": "1A", "sast_hint": "1A_sast_hint_full", "sast_hint_max_reps": None},
    "UDM": {"task_id": "task8_vuln_udm_full", "no_hint": "1A", "sast_hint": "1A_sast_hint_full", "sast_hint_max_reps": None},
}

# Manual expert review counts (docs/expert_review/03_CVE_CVSS_sast.md:306-320,
# Lorenzo, 2026-08-04) — NOT computable from code, cited here on purpose.
# NOTE: the call of 2026-08-20 mentions "13 nuove vulnerabilità... accettate
# dal maintainer" for the SAST-hint total, one point higher than Lorenzo's
# 12 here — likely a later maintainer-confirmation round not yet folded into
# doc 03. Flagged, not silently reconciled; confirm with the team before
# using these Candidates numbers in the paper as final.
CANDIDATES = {
    "no_hint": {"PCF": 0, "UDR": 4, "AMF": 2, "UDM": 4},
    "sast_hint": {"PCF": 0, "UDR": 4, "AMF": 2, "UDM": 6},
}


# Run combination that reproduces Tab. III of the ICAI-TEMS 2026 paper (TP/FN on
# all 8 rows). The no-hint arm is the pre-SGV `1A` run, overwritten on disk after
# that tag, so it can only be read back from git; UDR SAST-hint uses all 10 reps,
# unlike the canonical table above.
PAPER_ICAI_TAG = "results-2026-07-14"
PAPER_ICAI_NF_CONFIG: Dict[str, Dict[str, Any]] = {
    nf: {**cfg, "no_hint_ref": PAPER_ICAI_TAG, "sast_hint_max_reps": None} for nf, cfg in NF_CONFIG.items()
}
# The paper's Cand. column follows the class x NF matrix of doc 03, which counts
# CVE-2026-47780 as a UDR candidate (UDR 5), not the "10 / 10+2" totals above.
PAPER_ICAI_CANDIDATES = {
    "no_hint": {"PCF": 0, "UDR": 5, "AMF": 2, "UDM": 4},
    "sast_hint": {"PCF": 0, "UDR": 5, "AMF": 2, "UDM": 6},
}


def _corrected_dataset() -> Dict[str, Any]:
    """Production dataset with the two spurious UDR CVEs made unmatchable."""
    dataset = copy.deepcopy(cvss_eval.load_cvss_dataset())
    for cve in dataset.get("cves", []):
        if cve.get("id") in UDR_SPURIOUS_CVES:
            cve["handler_functions"] = []
    return dataset


def _load_repetitions(task_id: str, experiment_id: str, max_reps: Optional[int]) -> List[Dict[str, Any]]:
    agent_dir = Path(config.RESULTS_PATH) / task_id / experiment_id / "agent"
    files = sorted(agent_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"no raw JSON under {agent_dir}")
    data = json.loads(files[0].read_text(encoding="utf-8"))
    reps = data.get("repetitions", [])
    return reps[:max_reps] if max_reps else reps


def load_repetitions_from_git(ref: str, task_id: str, experiment_id: str, max_reps: Optional[int]) -> List[Dict[str, Any]]:
    """Repetitions of a run as frozen in a results-* tag (layout before rawJson/)."""
    path = f"results/{task_id}/{experiment_id}/agent/hosted_gemma4_31b_cloud.json"
    blob = subprocess.run(
        ["git", "show", f"{ref}:{path}"], capture_output=True, text=True, check=True,
        cwd=Path(__file__).resolve().parent.parent,
    ).stdout
    reps = json.loads(blob).get("repetitions", [])
    return reps[:max_reps] if max_reps else reps


def hit_counts(evals: List[Dict[str, Any]]) -> Dict[str, int]:
    """CVE id -> number of repetitions in which it is matched (0 included for
    every target CVE, so a never-found CVE still shows up)."""
    counts: Dict[str, int] = {}
    for e in evals:
        for m in e.get("matched", []):
            counts[m["cve_id"]] = counts.get(m["cve_id"], 0) + 1
        for c in e.get("missed_cves", []):
            counts.setdefault(c, 0)
    return dict(sorted(counts.items()))


def _evals(task_id: str, reps: List[Dict[str, Any]], dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Swap the module-level cache so evaluate_cvss_estimate/_candidate_cves
    # see `dataset` for this call only, then restore — avoids a permanent
    # monkeypatch leaking into anything else that imports cvss_eval.
    cvss_eval.load_cvss_dataset.cache_clear()
    original = cvss_eval.load_cvss_dataset
    cvss_eval.load_cvss_dataset = lambda path=None: dataset
    try:
        evals = [
            cvss_eval.evaluate_cvss_estimate(task_id, (r.get("final_answer") or {}).get("cvss_estimate"))
            for r in reps
        ]
        return [e for e in evals if e is not None]
    finally:
        cvss_eval.load_cvss_dataset = original
        cvss_eval.load_cvss_dataset.cache_clear()


def _aggregate_distinct(evals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Alternate unit of analysis: distinct CVE recovered at least once across
    all repetitions pooled (vs the pooled CVE-x-repetition unit above). Every
    repetition draws from the same fixed candidate set, so n_target_cves is
    read off the first eval — TP/FN don't multiply by rep count here.

    FP (distinct) dedups unmatched findings by function name across every
    repetition — a simpler, fully deterministic proxy for "the same
    underlying finding reported again" than the report pipeline's grouping
    (utils/evaluation_utils.py::_compute_finding_groups), which additionally
    runs an LLM semantic check on leftovers. This script stays offline/fast
    on purpose, so that check is intentionally not reproduced here — treat
    FP (distinct) as an upper bound on truly distinct false positives, not
    an exact figure.
    """
    n_target = evals[0]["n_target_cves"] if evals else 0
    matched_cve_ids = {m["cve_id"] for e in evals for m in e.get("matched", [])}
    unmatched_functions = {
        (u.get("function") or f"<no-function>#{i}")
        for e in evals
        for i, u in enumerate(e.get("unmatched", []))
    }
    tp = len(matched_cve_ids)
    fn = n_target - tp
    fp = len(unmatched_functions)
    precision = tp / (tp + fp) if (tp + fp) else None
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision}


def build_table(nf_config: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Dict[str, Dict[str, Dict[str, Any]]]]:
    corrected = _corrected_dataset()
    rows: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = {}
    for nf, cfg in (nf_config or NF_CONFIG).items():
        if cfg.get("no_hint_ref"):
            no_hint_reps = load_repetitions_from_git(cfg["no_hint_ref"], cfg["task_id"], cfg["no_hint"], None)
        else:
            no_hint_reps = _load_repetitions(cfg["task_id"], cfg["no_hint"], None)
        sast_hint_reps = _load_repetitions(cfg["task_id"], cfg["sast_hint"], cfg["sast_hint_max_reps"])
        rows[nf] = {}
        for cond_key, reps in (("no_hint", no_hint_reps), ("sast_hint", sast_hint_reps)):
            evals = _evals(cfg["task_id"], reps, corrected)
            rows[nf][cond_key] = {
                "pooled": cvss_eval.aggregate_detection_metrics(evals),
                "distinct": _aggregate_distinct(evals),
                # kept for the Precision@K view, which needs the per-repetition
                # ranking rather than the already-aggregated counts
                "evals": evals,
            }
    return rows


def _fmt_variant(rows: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]], variant: str, candidates=None) -> str:
    candidates = candidates or CANDIDATES
    lines = ["NF | Config | TP | FP | Cand. | FN | Prec. | DR", "---|---|---|---|---|---|---|---"]
    totals = {"no_hint": {"tp": 0, "fp": 0, "fn": 0, "cand": 0}, "sast_hint": {"tp": 0, "fp": 0, "fn": 0, "cand": 0}}
    for nf, by_cond in rows.items():
        for cond_key, cond_label in (("no_hint", "No-hint"), ("sast_hint", "SAST-hint")):
            m = by_cond[cond_key][variant]
            cand = candidates[cond_key][nf]
            tp, fp, fn = m["tp"], m["fp"], m["fn"]
            prec = m["precision"] or 0.0
            dr = cand / (tp + fp) if (tp + fp) else 0.0
            lines.append(f"{nf} | {cond_label} | {tp} | {fp} | {cand} | {fn} | {prec:.3f} | {dr:.3f}")
            totals[cond_key]["tp"] += tp
            totals[cond_key]["fp"] += fp
            totals[cond_key]["fn"] += fn
            totals[cond_key]["cand"] += cand
    for cond_key, cond_label in (("no_hint", "No-hint"), ("sast_hint", "SAST-hint")):
        t = totals[cond_key]
        prec = t["tp"] / (t["tp"] + t["fp"]) if (t["tp"] + t["fp"]) else 0.0
        dr = t["cand"] / (t["tp"] + t["fp"]) if (t["tp"] + t["fp"]) else 0.0
        lines.append(f"**Tot.** | {cond_label} | **{t['tp']}** | **{t['fp']}** | **{t['cand']}** | **{t['fn']}** | **{prec:.3f}** | **{dr:.3f}**")
    return "\n".join(lines)


def _fmt_precision_at_k(rows: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]]) -> str:
    """Precision@K on the same corrected dataset as the tables above.

    The published Tab.5 of `docs/sgv_protocol/10_/12_...tex` was computed on the
    raw dataset, i.e. before the `bd0dcc0` correction, so its UDR row counts the
    two spurious matches as true positives. Recomputing here keeps Precision@K
    consistent with the detection tables instead of leaving two numbers in the
    paper that disagree about what a UDR true positive is.
    """

    def _cell(entry: Dict[str, Any]) -> str:
        mean = entry["mean_precision_at_k"]
        frac = f"({entry['n_reps_with_k_findings']}/{entry['n_reps_total']})"
        return f"n/a {frac}" if mean is None else f"{mean * 100:.1f}% {frac}"

    lines = ["NF | Config | P@1 | P@3 | P@5", "---|---|---|---|---"]
    for cond_key, cond_label in (("no_hint", "No-hint"), ("sast_hint", "SAST-hint")):
        pooled_evals: List[Dict[str, Any]] = []
        for nf, by_cond in rows.items():
            evals = by_cond[cond_key]["evals"]
            pooled_evals += evals
            at_k = cvss_eval.aggregate_precision_at_k(evals)
            lines.append(f"{nf} | {cond_label} | " + " | ".join(_cell(at_k[k]) for k in (1, 3, 5)))
        at_k = cvss_eval.aggregate_precision_at_k(pooled_evals)
        lines.append(
            f"**Pooled** | {cond_label} | " + " | ".join(f"**{_cell(at_k[k])}**" for k in (1, 3, 5))
        )
    return "\n".join(lines)


def _fmt(rows: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]], candidates=None) -> str:
    return (
        "## Pooled (unit = CVE x repetition, TP/FP/FN summed across reps)\n\n"
        + _fmt_variant(rows, "pooled", candidates)
        + "\n\n## Distinct (unit = distinct CVE recovered at least once; FP = distinct unmatched function names)\n\n"
        + _fmt_variant(rows, "distinct", candidates)
        + "\n\n## Precision@K (final answer, ranked by the agent's own CVSS estimate)\n\n"
        + _fmt_precision_at_k(rows)
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--paper-icai", action="store_true",
        help=f"run combination of the ICAI-TEMS 2026 paper: no-hint from tag {PAPER_ICAI_TAG}, UDR SAST-hint 10 reps",
    )
    args = ap.parse_args()
    if args.paper_icai:
        print(_fmt(build_table(PAPER_ICAI_NF_CONFIG), PAPER_ICAI_CANDIDATES))
    else:
        print(_fmt(build_table()))
