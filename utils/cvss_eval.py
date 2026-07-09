"""Deterministic CVSS evaluation (Blocco B, experiment 2b).

Compares the classifier's CVSS 4.0 estimate against the ground-truth dataset
(`File_Free5gc_Vulnerabili/cve_metrics_normalized.json`) without any LLM:

1. finding <-> CVE matching by handler function name (docs/proposta_rubrica_cvss.md §7.3)
2. score proximity in bands, against both the published score (B or BT) and
   the recomputed pure-base score `base_score_B` where available
3. per-field vector match, split into exploitability (AV/AC/AT/PR/UI, 0-5)
   and impact (VC/VI/VA, 0-3) — the impact triad is what actually
   discriminates between the dataset CVEs

Results are reported separately from the rubric judge score (Blocco A) and
never influence the correct/wrong verdict.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import config

logger = logging.getLogger(__name__)

EXPLOITABILITY_METRICS = ["AV", "AC", "AT", "PR", "UI"]
IMPACT_METRICS = ["VC", "VI", "VA"]


@lru_cache(maxsize=1)
def load_cvss_dataset(path: Optional[str] = None) -> Dict[str, Any]:
    dataset_path = Path(path or config.CVSS_DATASET_PATH)
    return json.loads(dataset_path.read_text(encoding="utf-8"))


def _parse_vector(vector: str) -> Dict[str, str]:
    """Parse 'CVSS:4.0/AV:N/AC:L/...' into {'AV': 'N', 'AC': 'L', ...}."""
    parts = {}
    for chunk in vector.strip().split("/"):
        if ":" in chunk and not chunk.upper().startswith("CVSS"):
            key, value = chunk.split(":", 1)
            parts[key.strip().upper()] = value.strip().upper()
    return parts


def _score_band(estimated: float, reference: float) -> int:
    """Proximity band score: bands are (max_abs_delta, points), config-driven."""
    delta = abs(float(estimated) - float(reference))
    for max_delta, points in config.CVSS_SCORE_BANDS:
        if delta <= max_delta:
            return points
    return 0


def _candidate_cves(task_id: str) -> List[Dict[str, Any]]:
    """CVEs belonging to this task. `_full` task variants use the whole source
    file, so CVEs outside the excerpt (`in_task_excerpt: false`) are included
    there and excluded everywhere else."""
    dataset = load_cvss_dataset()
    is_full_variant = "full" in task_id
    candidates = []
    for cve in dataset.get("cves", []):
        cve_task = cve.get("task_id")
        if not cve_task or not task_id.startswith(cve_task):
            continue
        if cve.get("in_task_excerpt") or is_full_variant:
            candidates.append(cve)
    return candidates


def _match_finding(finding: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Match a finding to a candidate CVE by handler function name."""
    function = str(finding.get("function", "")).strip().lower()
    if function:
        for cve in candidates:
            for handler in cve.get("handler_functions") or []:
                h = handler.lower()
                if h in function or function in h:
                    return cve
    return None


def _evaluate_matched_pair(finding: Dict[str, Any], cve: Dict[str, Any]) -> Dict[str, Any]:
    gt_cvss = cve["cvss"]
    result: Dict[str, Any] = {"cve_id": cve["id"]}

    est_score = finding.get("score")
    if isinstance(est_score, (int, float)):
        est_score = float(est_score)
        result["estimated_score"] = est_score
        result["published_score"] = gt_cvss["base_score"]
        result["published_score_type"] = gt_cvss.get("score_type", "B")
        result["score_band_vs_published"] = _score_band(est_score, gt_cvss["base_score"])
        reference_b = gt_cvss.get("base_score_B") or gt_cvss["base_score"]
        result["score_band_vs_B"] = _score_band(est_score, reference_b)

    est_vector = finding.get("vector")
    if isinstance(est_vector, str) and est_vector.strip():
        est_metrics = _parse_vector(est_vector)
        gt_metrics = gt_cvss["base_metrics"]
        result["exploitability_match"] = sum(
            1 for m in EXPLOITABILITY_METRICS if est_metrics.get(m) == gt_metrics.get(m)
        )
        result["impact_match"] = sum(
            1 for m in IMPACT_METRICS if est_metrics.get(m) == gt_metrics.get(m)
        )
        result["estimated_vector"] = est_vector.strip()

    return result


def evaluate_cvss_estimate(task_id: str, estimate: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Evaluate the agent's CVSS estimate for one repetition.

    Returns None when the task has no CVEs in the dataset. Never raises:
    a malformed estimate yields an evaluation with zero matches.
    """
    candidates = _candidate_cves(task_id)
    if not candidates:
        return None

    findings = []
    if isinstance(estimate, dict):
        raw_findings = estimate.get("findings")
        if isinstance(raw_findings, list):
            findings = [f for f in raw_findings if isinstance(f, dict)]

    matched: List[Dict[str, Any]] = []
    unmatched_findings = 0
    remaining = list(candidates)

    # Single finding on a single-CVE task needs no function-name matching.
    if len(findings) == 1 and len(remaining) == 1:
        matched.append(_evaluate_matched_pair(findings[0], remaining[0]))
        remaining = []
    else:
        for finding in findings:
            cve = _match_finding(finding, remaining)
            if cve is None:
                unmatched_findings += 1
                continue
            matched.append(_evaluate_matched_pair(finding, cve))
            remaining = [c for c in remaining if c["id"] != cve["id"]]

    bands_published = [m["score_band_vs_published"] for m in matched if "score_band_vs_published" in m]
    bands_b = [m["score_band_vs_B"] for m in matched if "score_band_vs_B" in m]
    expl = [m["exploitability_match"] for m in matched if "exploitability_match" in m]
    impact = [m["impact_match"] for m in matched if "impact_match" in m]

    def _mean(values: List[float]) -> Optional[float]:
        return round(sum(values) / len(values), 3) if values else None

    return {
        "estimate_provided": bool(findings),
        "n_findings": len(findings),
        "n_target_cves": len(candidates),
        "matched": matched,
        "missed_cves": [c["id"] for c in remaining],
        "unmatched_findings": unmatched_findings,
        "aggregates": {
            "avg_score_band_vs_published": _mean(bands_published),
            "avg_score_band_vs_B": _mean(bands_b),
            "avg_exploitability_match": _mean(expl),  # 0-5
            "avg_impact_match": _mean(impact),  # 0-3
        },
    }
