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
    PYTHONPATH=. python utils/generate_detection_table.py
Output:
    Markdown + LaTeX table printed to stdout (not written to results/reports/
    — this is paper material, not a run report; copy it into
    docs/sgv_protocol/ by hand once reviewed).
"""

import copy
import json
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


def _aggregate(task_id: str, reps: List[Dict[str, Any]], dataset: Dict[str, Any]) -> Dict[str, Any]:
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
        evals = [e for e in evals if e is not None]
        return cvss_eval.aggregate_detection_metrics(evals)
    finally:
        cvss_eval.load_cvss_dataset = original
        cvss_eval.load_cvss_dataset.cache_clear()


def build_table() -> Dict[str, Dict[str, Dict[str, Any]]]:
    corrected = _corrected_dataset()
    rows: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for nf, cfg in NF_CONFIG.items():
        no_hint_reps = _load_repetitions(cfg["task_id"], cfg["no_hint"], None)
        sast_hint_reps = _load_repetitions(cfg["task_id"], cfg["sast_hint"], cfg["sast_hint_max_reps"])
        rows[nf] = {
            "no_hint": _aggregate(cfg["task_id"], no_hint_reps, corrected),
            "sast_hint": _aggregate(cfg["task_id"], sast_hint_reps, corrected),
        }
    return rows


def _fmt(rows: Dict[str, Dict[str, Dict[str, Any]]]) -> str:
    lines = ["NF | Config | TP | FP | Cand. | FN | Prec. | DR", "---|---|---|---|---|---|---|---"]
    totals = {"no_hint": {"tp": 0, "fp": 0, "fn": 0, "cand": 0}, "sast_hint": {"tp": 0, "fp": 0, "fn": 0, "cand": 0}}
    for nf, by_cond in rows.items():
        for cond_key, cond_label in (("no_hint", "No-hint"), ("sast_hint", "SAST-hint")):
            m = by_cond[cond_key]
            cand = CANDIDATES[cond_key][nf]
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


if __name__ == "__main__":
    result = build_table()
    print(_fmt(result))
