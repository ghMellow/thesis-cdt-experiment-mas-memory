"""Detection table for the multi-tool SAST input (gosec + Semgrep + CodeQL),
with and without the linked code, against the no-hint run, on UDR and UDM only:
AMF and PCF get no multi-tool alert on their ground-truth file, so their prompt
is the no-hint one.

Matching, the UDR spurious-match correction and both units of analysis come
from utils/generate_detection_table.py.

All arms are runs of the same day: the hosted model's serving changed since the
earlier runs (one repetition went from minutes to seconds), so they are not
comparable with these.

Usage:
    PYTHONPATH=. python utils/generate_multitool_table.py
"""

from typing import Dict, List, Optional, Tuple

from utils import generate_detection_table as paper

TASKS = {"UDR": "task6_vuln_udr_full", "UDM": "task8_vuln_udm_full"}

# arm -> experiment id
ARMS: Dict[str, str] = {
    "No-hint": "1A_no_hint_full_rerun2610",
    "3-tool": "1A_sast3tool_full",
    "3-tool + linked code": "1A_sast3tool_linked_full",
}

# (label, NF -> number of repetitions)
VIEWS: List[Tuple[str, Dict[str, int]]] = [("n=3", {"UDR": 3, "UDM": 3}), ("UDR n=10", {"UDR": 10})]


def _row(nf: str, experiment_id: str, n: int, dataset) -> Optional[Dict]:
    try:
        reps = paper._load_repetitions(TASKS[nf], experiment_id, n)
    except FileNotFoundError:
        return None
    if len(reps) < n:
        return None
    evals = paper._evals(TASKS[nf], reps, dataset)
    return {
        "pooled": paper.cvss_eval.aggregate_detection_metrics(evals),
        "distinct": paper._aggregate_distinct(evals),
        "cves": sorted({m["cve_id"] for e in evals for m in e.get("matched", [])}),
    }


def _fmt_prec(p) -> str:
    return "—" if p is None else f"{p:.3f}"


def build() -> str:
    dataset = paper._corrected_dataset()
    out: List[str] = []
    for view, nfs in VIEWS:
        out.append(f"### {view}\n")
        out.append("NF | Arm | Exp. id | TP | FP | FN | Prec. | TP dist. | FP dist. | FN dist. | CVE found")
        out.append("---|---|---|---|---|---|---|---|---|---|---")
        for nf, n in nfs.items():
            for arm, exp in ARMS.items():
                r = _row(nf, exp, n, dataset)
                if r is None:
                    out.append(f"{nf} | {arm} | `{exp}` | missing ({n} reps not on disk) |||||||")
                    continue
                p, d = r["pooled"], r["distinct"]
                out.append(
                    f"{nf} | {arm} | `{exp}` | {p['tp']} | {p['fp']} | {p['fn']} | {_fmt_prec(p['precision'])} | "
                    f"{d['tp']} | {d['fp']} | {d['fn']} | {', '.join(c.replace('CVE-2026-', '') for c in r['cves']) or '—'}"
                )
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    print(build())
