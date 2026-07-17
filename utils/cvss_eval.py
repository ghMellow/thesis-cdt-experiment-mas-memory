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
from typing import Any, Dict, List, Optional, Tuple, Union

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
    """Match a finding to a candidate CVE by handler function name.

    First-match semantics (call 13 follow-up): the caller consumes the CVE at
    the first finding whose function matches, in agent output order. When a
    repetition reports the same handler more than once, *which* finding gets
    paired to the GT (and thus feeds the S metrics) is that order — function
    name is the only identity available, so there is no GT-independent way to
    prefer one duplicate over another, and any GT-aware tie-break (e.g. pick
    the closest vector) would leak the GT into the pairing and bias S upward.
    M metrics are unaffected either way (the CVE counts as matched once, the
    other finding lands in unmatched)."""
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
    result: Dict[str, Any] = {
        "cve_id": cve["id"],
        "function": str(finding.get("function", "")).strip() or None,
    }
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

        # S1 (docs/sgv_protocol/00_proposta_relatore.md §5.2): exact match over
        # every metric the agent actually emitted (8 base, 11 when the
        # subsequent-system triad is present) — not padded, so older runs
        # without SC/SI/SA are judged only on the 8 they emitted.
        exact_scope = REQUESTED_METRICS + (
            SUBSEQUENT_METRICS if all(m in est_metrics for m in SUBSEQUENT_METRICS) else []
        )
        result["exact_match"] = all(est_metrics.get(m) == gt_metrics.get(m) for m in exact_scope)

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


def _describe_unmatched(finding: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone record for a finding with no GT CVE — the experts' use case
    (potential vulnerabilities not yet tied to a CVE). The estimated vector is
    rescored with the official math so these can be ranked for triage."""
    entry: Dict[str, Any] = {"function": str(finding.get("function", "")).strip() or None}
    score = finding.get("score")
    if isinstance(score, (int, float)):
        entry["declared_score"] = float(score)
    vector = finding.get("vector")
    if isinstance(vector, str) and vector.strip():
        entry["vector"] = vector.strip()
        computed, padded = compute_base_score(_parse_vector(vector))
        if computed is not None:
            entry["computed_score_B"] = computed
            if padded:
                entry["padded_metrics"] = padded
    return entry


def evaluate_cvss_estimate(task_id: str, estimate: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Evaluate the agent's CVSS estimate for one repetition.

    Returns None only when the task has no CVEs in the dataset AND the agent
    produced no estimate. On tasks without mapped CVEs (e.g. task9, F4) an
    estimate still yields an unmatched-only evaluation: every finding is
    rescored and ranked — the experts' use case. Never raises: a malformed
    estimate yields an evaluation with zero matches.
    """
    candidates = _candidate_cves(task_id)

    findings = []
    if isinstance(estimate, dict):
        raw_findings = estimate.get("findings")
        if isinstance(raw_findings, list):
            findings = [f for f in raw_findings if isinstance(f, dict)]

    if not candidates and not findings:
        return None

    matched: List[Dict[str, Any]] = []
    unmatched: List[Dict[str, Any]] = []
    remaining = list(candidates)

    # Single finding on a single-CVE task needs no function-name matching.
    if len(findings) == 1 and len(remaining) == 1:
        matched.append(_evaluate_matched_pair(findings[0], remaining[0]))
        remaining = []
    else:
        for finding in findings:
            cve = _match_finding(finding, remaining)
            if cve is None:
                unmatched.append(_describe_unmatched(finding))
                continue
            matched.append(_evaluate_matched_pair(finding, cve))
            remaining = [c for c in remaining if c["id"] != cve["id"]]

    # Triage order: most severe first, by the officially recomputed score
    # (declared score as fallback when the vector didn't rescore).
    unmatched.sort(
        key=lambda e: e.get("computed_score_B", e.get("declared_score", -1.0)) or -1.0,
        reverse=True,
    )

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
        "unmatched_findings": len(unmatched),
        "unmatched": unmatched,
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


def aggregate_detection_metrics(evals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """M1 (detection per CVE) + M2 (precision/recall/F1) over a list of
    `evaluate_cvss_estimate` results — the caller picks which attempt each
    eval came from (pass@1: first history entry: pass@k: the final one,
    already stored as `cvss_eval`), this function only aggregates.

    Unit of analysis is the CVE (docs/sgv_protocol/00_proposta_relatore.md
    §2/§5.1): TP = matched CVEs, FN = missed CVEs, FP = findings that paired
    to no candidate CVE (`unmatched` — includes genuine extra vulnerabilities
    with no catalogued CVE, not only false positives; see Blocco B legend).
    """
    with_targets = [e for e in evals if e.get("n_target_cves")]
    tp = sum(len(e.get("matched", [])) for e in evals)
    fn = sum(len(e.get("missed_cves", [])) for e in evals)
    fp = sum(e.get("unmatched_findings", 0) for e in evals)

    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision is not None and recall is not None and (precision + recall) > 0
        else None
    )

    detected = sum(1 for e in with_targets if len(e.get("matched", [])) > 0)
    coverage_ratios = [
        len(e.get("matched", [])) / e["n_target_cves"] for e in with_targets
    ]

    # M3 — alerts per TP: every finding the reviewer has to read (matched +
    # unmatched) for each true positive actually surfaced. Undefined when
    # nothing was ever matched (no TP to divide by).
    alerts_per_tp = (tp + fp) / tp if tp else None

    return {
        "n_reps": len(evals),
        "n_reps_with_targets": len(with_targets),
        "detection_rate": detected / len(with_targets) if with_targets else None,
        "avg_coverage": sum(coverage_ratios) / len(coverage_ratios) if coverage_ratios else None,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "alerts_per_tp": alerts_per_tp,
        "f1": f1,
    }


def _modal_vector(vectors: List[Dict[str, str]]) -> Dict[str, str]:
    """S3 null-model baseline: the most frequent value per metric across a
    set of GT vectors (ties broken by first-seen order — irrelevant when a
    task has a single target CVE, where the modal vector IS the GT vector by
    construction and the baseline degenerates to 100%; that degeneracy is a
    real property of the dataset, not a bug)."""
    from collections import Counter

    modal: Dict[str, str] = {}
    for metric in REQUESTED_METRICS + SUBSEQUENT_METRICS:
        values = [v[metric] for v in vectors if metric in v]
        if values:
            modal[metric] = Counter(values).most_common(1)[0][0]
    return modal


def aggregate_severity_metrics(task_ids: Union[str, List[str]], evals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """S1 (exact vector match), S2 (per-metric accuracy + ordinal distance),
    S3 (baseline: a null model that always guesses the modal GT vector) —
    §5.2 of the proposal, computed only on TP (matched findings).

    S3 needs the full set of GT vectors for the candidate CVEs of every task
    in scope (not just the ones the agent matched) since the baseline is a
    property of the dataset, not of what the agent happened to find — hence
    `task_ids` here rather than deriving everything from `evals`. Accepts
    either a single task_id (per-task report) or a list (pooled cross-task
    rollup, e.g. comparison.md): the baseline is the modal vector over the
    union of every task's candidate CVEs.
    """
    if isinstance(task_ids, str):
        task_ids = [task_ids]
    findings = [m for e in evals for m in e.get("matched", []) if "estimated_vector" in m]
    if not findings:
        return {}

    n = len(findings)
    s1 = sum(1 for f in findings if f.get("exact_match")) / n

    all_metrics = REQUESTED_METRICS + SUBSEQUENT_METRICS
    per_metric: Dict[str, Dict[str, Any]] = {}
    for metric in all_metrics:
        pairs = []
        for f in findings:
            est = _parse_vector(f["estimated_vector"])
            pub = _parse_vector(f.get("published_vector") or "")
            if metric in est and metric in pub:
                pairs.append((est[metric], pub[metric]))
        if not pairs:
            continue
        order = SEVERITY_ORDER[metric]
        per_metric[metric] = {
            "n": len(pairs),
            "accuracy": sum(1 for e, g in pairs if e == g) / len(pairs),
            "avg_distance": sum(
                abs(order.index(e) - order.index(g)) / (len(order) - 1)
                for e, g in pairs if e in order and g in order
            ) / len(pairs),
        }

    published_vectors = [_parse_vector(f.get("published_vector") or "") for f in findings]
    candidate_vectors = [
        cve["cvss"]["base_metrics"]
        for task_id in task_ids
        for cve in _candidate_cves(task_id)
        if cve.get("cvss", {}).get("base_metrics")
    ]
    modal = _modal_vector(candidate_vectors or published_vectors)

    baseline_exact = 0
    for pv in published_vectors:
        scope = [m for m in all_metrics if m in pv]
        if scope and all(modal.get(m) == pv.get(m) for m in scope):
            baseline_exact += 1
    baseline_per_metric: Dict[str, float] = {}
    for metric in all_metrics:
        pairs = [pv[metric] for pv in published_vectors if metric in pv]
        if pairs:
            baseline_per_metric[metric] = sum(1 for g in pairs if modal.get(metric) == g) / len(pairs)

    return {
        "n": n,
        "s1_exact_match": s1,
        "per_metric": per_metric,
        "modal_vector": modal,
        "s3_baseline_exact_match": baseline_exact / n,
        "s3_baseline_per_metric": baseline_per_metric,
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

            # M1/M2 pass@1: same evaluation, but against the *first* attempt's
            # estimate (history[0]) instead of the final one — lets the report
            # compare detection before vs. after the retry loop (docs/sgv_protocol/
            # 07_metriche_M_S_2026-07-14.md).
            history = rep.get("history")
            first_estimate = (
                history[0].get("cvss_estimate") if isinstance(history, list) and history else None
            )
            new_eval_pass1 = evaluate_cvss_estimate(task_id, first_estimate)
            if new_eval_pass1 is not None and new_eval_pass1 != rep.get("cvss_eval_pass1"):
                rep["cvss_eval_pass1"] = new_eval_pass1
                changed = True
        if changed:
            result_file.write_text(json.dumps(data, indent=2, ensure_ascii=True))
            updated += 1
            logger.info("Recomputed cvss_eval: %s", result_file)
    return updated


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()  # report regeneration may call the hosted semantic-check LLM
    # config reads the key at import time (before load_dotenv here): refresh it.
    config.OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    n = recompute_saved_results()
    logger.info("Updated %s result files, regenerating reports", n)
    from utils.evaluation_utils import _write_evaluation_reports

    _write_evaluation_reports(config.RESULTS_PATH)
    logger.info("Done")
