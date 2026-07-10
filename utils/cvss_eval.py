"""Deterministic CVSS evaluation (Blocco B, experiment 2b).

Compares the classifier's CVSS 4.0 estimate against the ground-truth dataset
(`File_Free5gc_Vulnerabili/cve_metrics_normalized.json`) without any LLM:

1. finding <-> CVE matching by handler function name (docs/proposta_rubrica_cvss.md §7.3)
2. score evaluation on three axes (call 11 — official CVSS 4.0 math via the
   `cvss` library, which implements the FIRST macrovector + lookup-table +
   interpolation algorithm):
   - `computed_score_B`: base score recomputed from the *estimated vector*
   - `score_coherence_delta`: |declared score - computed score| — internal
     consistency between the two things the agent emits (they are produced
     independently, nothing forces them to agree)
   - `computed_delta_vs_B` / `score_band_computed_vs_B`: distance between the
     recomputed score and the ground-truth pure base score — the vector
     comparison in official score space
   Legacy proximity bands on the *declared* score are kept for continuity.
3. per-field vector comparison, split into exploitability (AV/AC/AT/PR/UI)
   and impact (VC/VI/VA):
   - binary match counts (legacy, kept for continuity with runs 1-3 reports)
   - `exploitability_distance` / `impact_distance`: severity-aware ordinal
     distance in [0,1] per group (0 = identical, 1 = maximally distant) —
     "one level off" no longer counts the same as "opposite end of the scale"
   - `hamming_distance`: count of differing fields among the 8 requested

Results are reported separately from the rubric judge score (Blocco A) and
never influence the correct/wrong verdict.

Retroactive recompute (no re-run needed — estimates live in the saved JSONs):

    poetry run python -m utils.cvss_eval          # recompute + regenerate reports
"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cvss import CVSS4

import config

logger = logging.getLogger(__name__)

EXPLOITABILITY_METRICS = ["AV", "AC", "AT", "PR", "UI"]
IMPACT_METRICS = ["VC", "VI", "VA"]
SUBSEQUENT_METRICS = ["SC", "SI", "SA"]
# Vulnerable-system metrics; SC/SI/SA are requested too since 2026-07-10 but
# evaluated separately (subsequent_* fields) so runs 1-3 stay comparable —
# hamming_distance stays 0-8 on these for the same reason.
REQUESTED_METRICS = EXPLOITABILITY_METRICS + IMPACT_METRICS

# Allowed values per metric, ordered most severe -> least severe (CVSS 4.0
# specification §2). Used both to validate vectors and to compute the ordinal
# severity distance.
SEVERITY_ORDER: Dict[str, List[str]] = {
    "AV": ["N", "A", "L", "P"],
    "AC": ["L", "H"],
    "AT": ["N", "P"],
    "PR": ["N", "L", "H"],
    "UI": ["N", "P", "A"],
    "VC": ["H", "L", "N"],
    "VI": ["H", "L", "N"],
    "VA": ["H", "L", "N"],
    "SC": ["H", "L", "N"],
    "SI": ["H", "L", "N"],
    "SA": ["H", "L", "N"],
}


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


def compute_base_score(metrics: Dict[str, str]) -> Tuple[Optional[float], List[str]]:
    """Official CVSS 4.0 base score from parsed metrics via the `cvss` library
    (FIRST macrovector algorithm).

    The prompt asks for all 11 base metrics (SC/SI/SA included since
    2026-07-10); on older runs the subsequent-system metrics are padded with
    N when absent — every CVE in the ground-truth dataset has SC/SI/SA = N,
    so the padding never distorts the comparison. Returns
    (score, padded_metrics); score is None when a vulnerable-system metric is
    missing or invalid.
    """
    padded: List[str] = []
    parts = ["CVSS:4.0"]
    for metric in REQUESTED_METRICS + SUBSEQUENT_METRICS:
        value = metrics.get(metric)
        if value is None and metric in SUBSEQUENT_METRICS:
            value = "N"
            padded.append(metric)
        if value not in SEVERITY_ORDER[metric]:
            return None, padded
        parts.append(f"{metric}:{value}")
    try:
        return float(CVSS4("/".join(parts)).base_score), padded
    except Exception:  # malformed despite validation — never break a run
        logger.warning("CVSS4 scoring failed for vector %s", "/".join(parts))
        return None, padded


def _severity_distance(est: Dict[str, str], gt: Dict[str, str], group: List[str]) -> float:
    """Mean ordinal distance over a metric group, each metric normalized to
    [0,1] by its scale length. A missing/invalid estimated value counts as
    maximally distant (1.0)."""
    distances = []
    for metric in group:
        order = SEVERITY_ORDER[metric]
        e_val, g_val = est.get(metric), gt.get(metric)
        if e_val not in order or g_val not in order:
            distances.append(1.0)
            continue
        distances.append(abs(order.index(e_val) - order.index(g_val)) / (len(order) - 1))
    return round(sum(distances) / len(distances), 3)


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
    # Pure base reference: base_score_B where published score is BT, else the
    # published score itself (already type B).
    reference_b = gt_cvss.get("base_score_B") or gt_cvss["base_score"]

    est_score = finding.get("score")
    if isinstance(est_score, (int, float)):
        est_score = float(est_score)
        result["estimated_score"] = est_score
        result["published_score"] = gt_cvss["base_score"]
        result["published_score_type"] = gt_cvss.get("score_type", "B")
        result["score_band_vs_published"] = _score_band(est_score, gt_cvss["base_score"])
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
        result["published_vector"] = gt_cvss.get("vector")

        # Severity-aware vector distance (call 11): ordinal, per group, in [0,1].
        result["exploitability_distance"] = _severity_distance(
            est_metrics, gt_metrics, EXPLOITABILITY_METRICS
        )
        result["impact_distance"] = _severity_distance(est_metrics, gt_metrics, IMPACT_METRICS)

        # Subsequent-system triad: only scored when the agent actually emitted
        # it (prompt asks for it since 2026-07-10). Padding would auto-match
        # the GT (always N there) and hand out free points on older runs.
        if all(m in est_metrics for m in SUBSEQUENT_METRICS):
            result["subsequent_match"] = sum(
                1 for m in SUBSEQUENT_METRICS if est_metrics.get(m) == gt_metrics.get(m)
            )
            result["subsequent_distance"] = _severity_distance(
                est_metrics, gt_metrics, SUBSEQUENT_METRICS
            )
        result["hamming_distance"] = sum(
            1 for m in REQUESTED_METRICS if est_metrics.get(m) != gt_metrics.get(m)
        )

        # Official score recomputed from the estimated vector (FIRST 4.0 math).
        computed, padded = compute_base_score(est_metrics)
        if computed is not None:
            result["computed_score_B"] = computed
            if padded:
                result["padded_metrics"] = padded
            result["computed_delta_vs_B"] = round(abs(computed - reference_b), 1)
            result["score_band_computed_vs_B"] = _score_band(computed, reference_b)
            if "estimated_score" in result:
                result["score_coherence_delta"] = round(
                    abs(result["estimated_score"] - computed), 1
                )

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

    def _collect(key: str) -> List[float]:
        return [m[key] for m in matched if isinstance(m.get(key), (int, float))]

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
            "avg_score_band_vs_published": _mean(_collect("score_band_vs_published")),
            "avg_score_band_vs_B": _mean(_collect("score_band_vs_B")),
            "avg_exploitability_match": _mean(_collect("exploitability_match")),  # 0-5
            "avg_impact_match": _mean(_collect("impact_match")),  # 0-3
            # Official-math axes (call 11):
            "avg_score_coherence_delta": _mean(_collect("score_coherence_delta")),
            "avg_computed_delta_vs_B": _mean(_collect("computed_delta_vs_B")),
            "avg_score_band_computed_vs_B": _mean(_collect("score_band_computed_vs_B")),
            "avg_exploitability_distance": _mean(_collect("exploitability_distance")),  # 0-1
            "avg_impact_distance": _mean(_collect("impact_distance")),  # 0-1
            "avg_subsequent_match": _mean(_collect("subsequent_match")),  # 0-3, only when emitted
            "avg_subsequent_distance": _mean(_collect("subsequent_distance")),  # 0-1, only when emitted
            "avg_hamming_distance": _mean(_collect("hamming_distance")),  # 0-8
        },
    }


def recompute_saved_results(results_path: Optional[str] = None) -> int:
    """Recompute `cvss_eval` in-place on every saved repetition — the agent's
    estimate lives in `final_answer.cvss_estimate`, so new evaluation logic
    applies retroactively without re-running any experiment. Returns the
    number of repetitions updated."""
    root = Path(results_path or config.RESULTS_PATH)
    updated = 0
    for result_file in sorted(root.glob("task*/*/*/*.json")):
        if result_file.name.endswith("_solution.json"):
            continue
        data = json.loads(result_file.read_text(encoding="utf-8"))
        repetitions = data.get("repetitions") if isinstance(data.get("repetitions"), list) else [data]
        task_id = data.get("task_id", "")
        changed = False
        for rep in repetitions:
            estimate = (rep.get("final_answer") or {}).get("cvss_estimate")
            if estimate is None and "cvss_eval" not in rep:
                continue
            new_eval = evaluate_cvss_estimate(task_id, estimate)
            if new_eval is not None and new_eval != rep.get("cvss_eval"):
                rep["cvss_eval"] = new_eval
                changed = True
        if changed:
            result_file.write_text(json.dumps(data, indent=2, ensure_ascii=True))
            updated += 1
            logger.info("Recomputed cvss_eval: %s", result_file)
    return updated


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    n = recompute_saved_results()
    logger.info("Updated %s result files, regenerating reports", n)
    from utils.evaluation_utils import _write_evaluation_reports

    _write_evaluation_reports(config.RESULTS_PATH)
    logger.info("Done")
