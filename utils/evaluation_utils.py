"""Evaluation report helpers — anomaly-focused output."""

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import config
from config import RESULTS_PATH

logger = logging.getLogger(__name__)


def _record_consistency_finding(lines: List[str]) -> None:
    if not lines:
        return
    eval_path = Path(RESULTS_PATH) / "evaluation" / "consistency.md"
    eval_path.parent.mkdir(parents=True, exist_ok=True)
    existing = eval_path.read_text(encoding="utf-8") if eval_path.exists() else ""
    content = existing + "\n" + "\n".join(lines) + "\n"
    eval_path.write_text(content.strip() + "\n", encoding="utf-8")


def _collect_results(
    results_path: str, run_id: Optional[str] = None
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """Scan results/ into {experiment_id: {role: [payloads]}}.

    run_id: when set, keep only repetitions tagged with this exact run_id
    (main.py stamps every repetition of one invocation with the same id,
    independent of folder naming — use this instead of relying on which
    role-folder a result happens to live in, e.g. when several runs share
    the same task/experiment and only manual folder renaming told them apart).
    """
    base = Path(results_path)
    data: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    if not base.exists():
        return data
    _SKIP = {"evaluation"}
    for task_dir in sorted(p for p in base.iterdir() if p.is_dir() and p.name not in _SKIP):
        for experiment_dir in sorted(p for p in task_dir.iterdir() if p.is_dir()):
            experiment_id = experiment_dir.name
            data.setdefault(experiment_id, {})
            for role_dir in sorted(p for p in experiment_dir.iterdir() if p.is_dir()):
                role = role_dir.name
                result_files = sorted(role_dir.glob("*.json"))
                data[experiment_id].setdefault(role, [])
                for f in result_files:
                    try:
                        file_data = json.loads(f.read_text(encoding="utf-8"))
                    except Exception:
                        continue
                    if "repetitions" in file_data:
                        # New format: single file with run_config + repetitions array
                        run_config = {k: v for k, v in file_data.items() if k != "repetitions"}
                        for rep in file_data["repetitions"]:
                            merged = {**run_config, **rep}
                            if run_id is not None and merged.get("run_id") != run_id:
                                continue
                            data[experiment_id][role].append(merged)
                    else:
                        # Old format: one file per repetition (no run_id — never matches a filter)
                        if run_id is None:
                            data[experiment_id][role].append(file_data)
    return data


def list_runs(results_path: str) -> List[Tuple[str, str, str, str, int, str]]:
    """List distinct (task_id, experiment_id, role, run_id) groups found under
    results_path, with repetition count and the earliest started_at — the
    lookup table for `--run-id` filtering and for `06_*`/`07_*`-style findings
    docs, so identifying "which data is this run" doesn't need an ad hoc
    script each time."""
    base = Path(results_path)
    groups: Dict[Tuple[str, str, str, str], List[str]] = {}
    if not base.exists():
        return []
    for task_dir in sorted(p for p in base.iterdir() if p.is_dir() and p.name != "evaluation"):
        for experiment_dir in sorted(p for p in task_dir.iterdir() if p.is_dir()):
            for role_dir in sorted(p for p in experiment_dir.iterdir() if p.is_dir()):
                for f in sorted(role_dir.glob("*.json")):
                    try:
                        file_data = json.loads(f.read_text(encoding="utf-8"))
                    except Exception:
                        continue
                    reps = file_data.get("repetitions", [file_data])
                    for rep in reps:
                        key = (
                            task_dir.name,
                            experiment_dir.name,
                            role_dir.name,
                            rep.get("run_id") or "(no run_id — legacy result)",
                        )
                        groups.setdefault(key, []).append(rep.get("started_at") or "")
    return sorted(
        (task, exp, role, run, len(starts), min(s for s in starts if s) if any(starts) else "")
        for (task, exp, role, run), starts in groups.items()
    )


def _avg(values: List[float]) -> Optional[float]:
    return sum(values) / len(values) if values else None


def _fmt(value: Optional[float], digits: int = 2) -> str:
    return f"{value:.{digits}f}" if value is not None else "n/a"


def _fmt_ratio(value: Optional[float]) -> str:
    return f"{value:.1%}" if value is not None else "n/a"


def _fmt_delta(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1%}"


def _detect_inconsistencies(
    roles: Dict[str, List[Dict[str, Any]]],
    semantic_check: bool = True,
    task_filter: Optional[List[str]] = None,
) -> Tuple[List[Tuple[str, str, List[Tuple[int, str]], str]], int]:
    """Detect tasks with inconsistent reasoning across repetitions.

    Phase 1 (always): string equality filter — fast, catches all surface differences.
    Phase 2 (if semantic_check=True): LLM confirms whether flagged items are truly
    semantically different or just paraphrases.

    Args:
        roles: dict of {role: [payloads]}
        semantic_check: whether to use LLM for disambiguation
        task_filter: optional list of task_ids to evaluate (None = all)

    Returns:
        truly_inconsistent: list of (role, task_id, [(rep, reasoning),...], llm_explanation)
        n_surface_equiv: count of surface-different tasks confirmed semantically equivalent
    """
    surface_different: List[Tuple[str, str, List[Tuple[int, str]]]] = []
    for role, payloads in roles.items():
        per_task: Dict[str, List[Dict[str, Any]]] = {}
        for p in payloads:
            per_task.setdefault(p.get("task_id", "unknown"), []).append(p)
        for task_id, task_payloads in sorted(per_task.items()):
            if task_filter is not None and task_id not in task_filter:
                continue
            rep_reasonings: List[Tuple[int, str]] = []
            for p in task_payloads:
                fa = p.get("final_answer", {})
                r = fa.get("reasoning") if isinstance(fa, dict) else None
                if isinstance(r, str) and r.strip():
                    rep_reasonings.append((p.get("repetition", 0), r.strip()))
            if len({r for _, r in rep_reasonings}) > 1:
                surface_different.append((role, task_id, rep_reasonings))

    if not semantic_check or not surface_different:
        return [(role, tid, reps, "") for role, tid, reps in surface_different], 0

    from agents.judge_agent import run_semantic_equivalence_check
    from agents._llm_utils import resolve_model_config

    cache_path = Path(RESULTS_PATH) / "evaluation" / "semantic_cache.json"
    cache: Dict[str, Any] = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    if "semantic_check" not in config.MODELS:
        raise ValueError("MODELS['semantic_check'] must be set for semantic consistency checks")
    model, sem_is_hosted = resolve_model_config("semantic_check")
    base_url = config.OLLAMA_BASE_URL

    truly_inconsistent: List[Tuple[str, str, List[Tuple[int, str]], str]] = []
    n_surface_equiv = 0
    cache_updated = False

    logger.info(
        "Semantic consistency check: %d task(s) surface-different → calling judge",
        len(surface_different),
    )
    for i, (role, task_id, rep_reasonings) in enumerate(surface_different, 1):
        reasonings = [r for _, r in rep_reasonings]
        cache_key = (
            f"{role}/{task_id}/"
            + hashlib.sha256(json.dumps(reasonings).encode()).hexdigest()[:16]
        )
        if cache_key in cache:
            result = cache[cache_key]
            logger.info(
                "  [%d/%d] %s/%s — cache hit",
                i, len(surface_different), role, task_id,
            )
        else:
            logger.info(
                "  [%d/%d] %s/%s — judge (%d reps)",
                i, len(surface_different), role, task_id, len(rep_reasonings),
            )
            result = run_semantic_equivalence_check(
                task_id=f"{role}/{task_id}",
                reasonings=reasonings,
                model=model,
                base_url=base_url,
                is_hosted=sem_is_hosted,
            )
            cache[cache_key] = result
            cache_updated = True

        verdict = "equiv" if result.get("equivalent", False) else "differ"
        explanation = result.get("explanation", "")
        logger.info("  → %s | %s", verdict, explanation)
        if result.get("equivalent", False):
            n_surface_equiv += 1
        else:
            truly_inconsistent.append((role, task_id, rep_reasonings, result.get("explanation", "")))

    if cache_updated:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")

    return truly_inconsistent, n_surface_equiv


def _brier_score(payloads: List[Dict[str, Any]]) -> Optional[float]:
    """Mean squared error between confidence and actual correctness (lower = better calibrated)."""
    vals = [
        (float(fa["confidence"]) - (1.0 if p.get("verdict") == "correct" else 0.0)) ** 2
        for p in payloads
        if isinstance((fa := p.get("final_answer", {})), dict)
        and isinstance(fa.get("confidence"), (int, float))
    ]
    return _avg(vals)


def _build_scores_table(roles: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    # Determine task types present
    all_payloads = [p for payloads in roles.values() for p in payloads]
    task_types = set(p.get("task_type") for p in all_payloads if p.get("task_type"))
    is_pure_math = task_types == {"math"}
    is_pure_textual = task_types == {"textual"}
    
    # Build header based on task type
    if is_pure_math:
        header = "| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_math_delta |"
        sep = "| --- | --- | --- | --- | --- | --- |"
    elif is_pure_textual:
        header = "| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |"
        sep = "| --- | --- | --- | --- | --- | --- |"
    else:  # mixed
        header = "| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_math_delta | avg_textual_norm |"
        sep = "| --- | --- | --- | --- | --- | --- | --- |"
    
    lines = ['<a id="rubric-scores"></a>', "### Scores by role", "", header, sep]
    
    for role, payloads in sorted(roles.items()):
        total = len(payloads)
        correct = sum(1 for p in payloads if p.get("verdict") == "correct")
        avg_attempts = _avg([float(p.get("attempts", 1)) for p in payloads])
        confidences = [
            float(fa["confidence"])
            for p in payloads
            if isinstance((fa := p.get("final_answer", {})), dict)
            and isinstance(fa.get("confidence"), (int, float))
        ]
        textual_norms = []
        for p in payloads:
            if p.get("task_type") != "textual":
                continue
            js = p.get("judge_score", {})
            norm = js.get("normalized_score")
            if isinstance(norm, (int, float)):
                textual_norms.append(float(norm))
        math_deltas = [
            float(p["judge_score"]["delta"])
            for p in payloads
            if p.get("task_type") == "math"
            and isinstance(p.get("judge_score", {}).get("delta"), (int, float))
        ]
        
        if is_pure_math:
            lines.append(
                f"| {role} | {_fmt_ratio(correct / total if total else None)} | "
                f"{_fmt(_avg(confidences), 3)} | {_fmt(_brier_score(payloads), 4)} | "
                f"{_fmt(avg_attempts, 2)} | "
                f"{_fmt(_avg(math_deltas), 3)} |"
            )
        elif is_pure_textual:
            lines.append(
                f"| {role} | {_fmt_ratio(correct / total if total else None)} | "
                f"{_fmt(_avg(confidences), 3)} | {_fmt(_brier_score(payloads), 4)} | "
                f"{_fmt(avg_attempts, 2)} | "
                f"{_fmt(_avg(textual_norms), 3)} |"
            )
        else:  # mixed
            lines.append(
                f"| {role} | {_fmt_ratio(correct / total if total else None)} | "
                f"{_fmt(_avg(confidences), 3)} | {_fmt(_brier_score(payloads), 4)} | "
                f"{_fmt(avg_attempts, 2)} | "
                f"{_fmt(_avg(math_deltas), 3)} | {_fmt(_avg(textual_norms), 3)} |"
            )
    lines += [
        "",
        "**Legend**",
        "",
        "| metric | scope | meaning |",
        "| --- | --- | --- |",
        "| `accuracy` | all | share of repetitions with verdict = correct |",
        "| `avg_confidence` | all | mean self-reported confidence (0–1) |",
        "| `brier_score` | all | mean((confidence − is\\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |",
        "| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |",
        "| `avg_math_delta` | math | mean \\|answer − ground\\_truth\\| on math tasks — lower = more precise |",
        "| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |",
    ]
    return lines


def _build_cost_metrics_section(roles: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    """M5 — computational cost: tokens and wall-clock time per repetition
    (docs/sgv_protocol/00_proposta_relatore.md §5.1, 07_metriche_M_S_2026-07-14.md).
    Unlike M1-M3/S1-S3 this applies to every task type, not just CVSS ones —
    every repetition is timed, and token-counted whenever the backend reports it."""

    def _mean(values) -> Optional[float]:
        vals = [v for v in values if isinstance(v, (int, float))]
        return sum(vals) / len(vals) if vals else None

    lines = [
        '<a id="cost-metrics"></a>',
        "### Cost (M5)",
        "",
        "| role | n | avg elapsed (s) | avg agent tokens in | avg agent tokens out | avg judge tokens in | avg judge tokens out |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    any_data = False
    for role, payloads in sorted(roles.items()):
        if not payloads:
            continue
        any_data = True
        elapsed = _mean(p.get("elapsed_seconds") for p in payloads)
        agent_in = _mean((p.get("tokens") or {}).get("agent_in") for p in payloads)
        agent_out = _mean((p.get("tokens") or {}).get("agent_out") for p in payloads)
        judge_in = _mean((p.get("tokens") or {}).get("judge_in") for p in payloads)
        judge_out = _mean((p.get("tokens") or {}).get("judge_out") for p in payloads)
        lines.append(
            f"| {role} | {len(payloads)} | {_fmt(elapsed, 1)} | "
            f"{_fmt(agent_in, 0)} | {_fmt(agent_out, 0)} | "
            f"{_fmt(judge_in, 0)} | {_fmt(judge_out, 0)} |"
        )
    if not any_data:
        return []
    lines += [
        "",
        "**Legend**",
        "",
        "- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.",
        "- `n` = repetitions included, across every task type (not restricted to CVSS tasks).",
        "- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every "
        "attempt when a retry (SGV or rubric) was triggered.",
        "- Token columns = mean prompt/completion tokens the backend reported for the agent "
        "and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama "
        "Cloud runs in this project — the field is requested but not always populated, unlike "
        "local Ollama which reports it reliably).",
        "",
    ]
    return lines


def _build_sgv_section(all_payloads: List[Dict[str, Any]]) -> List[str]:
    """SGV (docs/sgv_protocol/): deterministic in-loop gate, no ground truth,
    reported separately from the rubric retries below. Current design choice
    (2026-07-14, see doc 06): a finding that never passes G1-G4 within
    MAX_RETRIES is NOT discarded — it's still scored downstream. This
    section is how that gets surfaced instead of silently disappearing into
    the raw JSON's per-attempt `sgv_eval`."""
    per_rep = []
    for p in all_payloads:
        sgv_events = [h.get("sgv_eval") for h in (p.get("history") or []) if h.get("sgv_eval") is not None]
        if not sgv_events:
            continue
        n_fail_attempts = sum(1 for e in sgv_events if not e.get("passed", True))
        per_rep.append((p, n_fail_attempts, sgv_events[-1]))

    if not per_rep:
        return []

    triggered = [(p, n, final) for p, n, final in per_rep if n > 0]
    still_failing = [(p, n, final) for p, n, final in triggered if not final.get("passed", True)]

    lines = [
        '<a id="sgv"></a>',
        "## SGV — Syntactic Grounding Verifier (Blocco C, deterministic, no ground truth)",
        "",
        "| metric | value |",
        "| --- | --- |",
        f"| repetitions with at least one SGV retry | {len(triggered)} |",
        f"| repetitions where SGV never passed (scored downstream anyway) | {len(still_failing)} |",
        "",
    ]

    if still_failing:
        lines += [f"#### Let through despite failing G1–G4 ({len(still_failing)})", ""]
        lines += [
            "| role | task_id | rep | attempts | failing finding | checks |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for p, n, final in still_failing:
            for pf in final.get("per_finding", []):
                if pf.get("passed", True):
                    continue
                bad = "; ".join(f"{k}: {v}" for k, v in pf.get("checks", {}).items() if v != "ok")
                lines.append(
                    f"| {p['_role']} | {p.get('task_id')} | {p.get('repetition')} | "
                    f"{p.get('attempts')} | `{pf.get('function')}` | {bad} |"
                )
        lines += [
            "",
            "**Legend**",
            "",
            "- These findings failed G1–G4 on every attempt up to `MAX_RETRIES` and were still passed on to the rubric judge and the CVSS matching above — the SGV never discards, it only flags (design choice, see `docs/sgv_protocol/06_implementazione_2026-07-14.md`).",
            "- `checks` = which G1–G4 check failed on the last attempt, and why.",
            "",
        ]

    resolved = [(p, n, final) for p, n, final in triggered if final.get("passed", True)]
    if resolved:
        lines += [f"#### Retries resolved by the agent ({len(resolved)})", ""]
        lines += [
            "| role | task_id | rep | attempts | fixed on attempt |",
            "| --- | --- | --- | --- | --- |",
        ]
        for p, n, final in resolved:
            lines.append(
                f"| {p['_role']} | {p.get('task_id')} | {p.get('repetition')} | "
                f"{p.get('attempts')} | {p.get('attempts')} |"
            )
        lines.append("")

    return lines


def _build_cvss_section(
    roles: Dict[str, List[Dict[str, Any]]], experiment_id: str, results_path: str
) -> List[str]:
    """CVSS sub-scores (Blocco B, deterministic) — reported separately from the
    rubric judge scores, never merged into accuracy."""
    has_cvss = any(
        isinstance(p.get("cvss_eval"), dict) for payloads in roles.values() for p in payloads
    )
    if not has_cvss:
        return []

    def _role_rows():
        for role, payloads in sorted(roles.items()):
            evals = [p["cvss_eval"] for p in payloads if isinstance(p.get("cvss_eval"), dict)]
            if evals:
                yield role, evals

    def _agg_mean(evals, key: str) -> Optional[float]:
        vals = [
            e["aggregates"][key]
            for e in evals
            if isinstance(e.get("aggregates", {}).get(key), (int, float))
        ]
        return _avg(vals)

    lines = ['<a id="cvss-estimate"></a>', "## CVSS estimate (Blocco B, deterministic)", ""]
    # Recurrence labels computed once so the letters are consistent between the
    # matched (vector detail) and unmatched tables (call 13 follow-up).
    matched_labels, unmatched_markers = _compute_finding_groups(roles)
    lines += _build_cvss_vector_detail(roles, experiment_id, results_path, matched_labels=matched_labels)
    lines += _build_cvss_unmatched(roles, experiment_id, results_path, unmatched_markers=unmatched_markers)

    # All the tables below are roll-ups over every repetition of the task —
    # M1-M3/S1-S3 included (per-role rows, TP pooled across reps), not
    # per-repetition detail. One umbrella heading makes the hierarchy explicit:
    # headline metrics (advisor's proposal) first, legacy diagnostics last
    # (2026-07-16 feedback: "Aggregate metrics" alone read as *the* aggregates,
    # as if M/S were something else).
    lines += [
        '<a id="metrics-across-reps"></a>',
        "### Metrics across repetitions",
        "",
        "_Every table in this section aggregates over all repetitions of the task "
        "(one row per role); the per-finding detail is above._",
        "",
    ]
    lines += _build_detection_metrics_section(roles, heading="####")
    lines += _build_cve_rep_matrix(roles, heading="####")
    lines += _build_retry_channel_section(roles, heading="####")
    lines += _build_sgv_detection_cross_section(roles, heading="####")
    lines += _build_severity_metrics_section(roles, heading="####")

    lines += [
        '<a id="legacy-diagnostics"></a>',
        "#### Legacy diagnostics (runs 1–3 comparability)",
        "",
        "_Diagnostic roll-up kept for comparability with runs 1–3, useful for a "
        "global read once you've checked the detail above isn't spitting "
        "nonsense — the headline metrics are M1–M3/S1–S3 above._",
        "",
        '<a id="estimates-vs-gt"></a>',
        "##### Estimates vs ground truth",
        "",
        "| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for role, evals in _role_rows():
        n_provided = sum(1 for e in evals if e.get("estimate_provided"))
        n_matched = sum(len(e.get("matched", [])) for e in evals)
        n_missed = sum(len(e.get("missed_cves", [])) for e in evals)
        n_unmatched = sum(e.get("unmatched_findings", 0) for e in evals)
        lines.append(
            f"| {role} | {n_provided}/{len(evals)} | {n_matched} | {n_missed} | {n_unmatched} | "
            f"{_fmt(_agg_mean(evals, 'avg_score_band_vs_published'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_score_band_vs_B'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_exploitability_match'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_impact_match'), 2)} |"
        )
    lines += [
        "",
        "**Legend**",
        "",
        "- `estimates` = X/Y — X = repetitions where the agent emitted *at least one* "
        "CVSS finding block; Y = total repetitions evaluated for this task. **This is "
        "block presence, not correctness** — it says nothing about how many "
        "vulnerabilities were actually found or matched (see `matched`/`missed CVEs` "
        "below for that).",
        "- `matched` = total findings, summed across all repetitions, successfully "
        "paired to a ground-truth CVE (by comparing the function name the agent "
        "reported to that CVE's known handler function).",
        "- `missed CVEs` = total ground-truth CVEs, summed across all repetitions, that "
        "no finding in that repetition matched — i.e. vulnerabilities the agent failed "
        "to surface at all.",
        "- `unmatched findings` = total findings, summed across all repetitions, that "
        "matched no ground-truth CVE — either a false positive, or a genuine extra "
        "vulnerability with no catalogued CVE (ranked for triage in the table further "
        "down).",
        "- ⚠️ **The remaining four columns are diagnostic only, not the headline "
        "metric**: `avg band vs published` / `avg band vs B` score how close the "
        "*declared* score is to the reference (0 = far, 3 = exact band), and "
        "`avg exploitability` (0-5) / `avg impact` (0-3) count binary field matches on "
        "the estimated vector. The declared score is produced independently of the "
        "vector the agent also emits and carries no official rigor of its own (F17: "
        "systematically lower than what the vector is actually worth). These four "
        "columns exist only for comparability with runs 1-3.",
        "- The metrics that actually count — recomputed from the vector with the "
        "official CVSS 4.0 algorithm — are in the table below.",
        "",
        '<a id="official-cvss-math"></a>',
        "##### Official CVSS 4.0 math (score recomputed from the estimated vector) — the reference metrics",
        "",
        "| role | avg coherence Δ (score↔vector) | avg computed Δ vs B | avg band computed vs B (0-3) | avg expl. distance (0-1) | avg impact distance (0-1) | avg subseq. distance (0-1) | avg Hamming (0-8) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for role, evals in _role_rows():
        lines.append(
            f"| {role} | {_fmt(_agg_mean(evals, 'avg_score_coherence_delta'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_computed_delta_vs_B'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_score_band_computed_vs_B'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_exploitability_distance'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_impact_distance'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_subsequent_distance'), 2)} | "
            f"{_fmt(_agg_mean(evals, 'avg_hamming_distance'), 2)} |"
        )
    lines += [
        "",
        "**Legend**",
        "",
        "- The estimated vector is rescored with the official FIRST CVSS 4.0 algorithm "
        "(macrovector + lookup table, `cvss` library).",
        "- `coherence Δ` = |score declared by the agent − score its own vector actually "
        "produces| (the two outputs are independent, nothing forces them to agree).",
        "- `computed Δ vs B` compares the recomputed score against the ground-truth pure "
        "base score — a vector distance in official score space.",
        "- Severity distances are ordinal and normalized per metric group (0 = identical "
        "vector, 1 = every field at the opposite end of its scale).",
        "- The subsequent-system triad SC/SI/SA is part of the required vector; its "
        "distance is scored only when the agent's estimate actually includes all "
        "three fields (older/legacy runs may lack them, shown as `n/a`).",
        "- Hamming counts plainly differing fields among the 8 vulnerable-system metrics "
        "(n/a = older runs, recompute with `python -m utils.cvss_eval`).",
        "",
    ]
    return lines


def _build_detection_metrics_section(roles: Dict[str, List[Dict[str, Any]]], heading: str = "###") -> List[str]:
    """M1 (detection per CVE) + M2 (precision/recall/F1) + M3 (alerts per TP),
    final answer vs first attempt (docs/sgv_protocol/00_proposta_relatore.md
    §5.1, 07_metriche_M_S_2026-07-14.md; renamed from pass@k/pass@1 per call
    13 — the system is evaluated as a black box on its final accepted answer,
    and "pass@k" wrongly suggested best-of-k independent samples). The
    headline row is the final answer (after every SGV + rubric retry, same
    data as `cvss_eval` above); "first attempt" is the diagnostic
    counterfactual (history[0], as if the retry loop didn't exist) — the gap
    between the two is the retry loop's actual effect on detection, the
    empirical question the proposal leaves open in §4's observation."""
    from utils.cvss_eval import aggregate_detection_metrics

    def _role_evals(key: str):
        for role, payloads in sorted(roles.items()):
            evals = [p[key] for p in payloads if isinstance(p.get(key), dict)]
            if evals:
                yield role, evals

    pass1_present = any(True for _ in _role_evals("cvss_eval_pass1"))
    if not pass1_present:
        return []

    lines = [
        '<a id="detection-metrics"></a>',
        f"{heading} Detection (M1, M2, M3 — final answer vs first attempt)",
        "",
        "| role | answer | reps | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    pass1_by_role = dict(_role_evals("cvss_eval_pass1"))
    passk_by_role = dict(_role_evals("cvss_eval"))
    for role in sorted(set(pass1_by_role) | set(passk_by_role)):
        for label, evals in (("final answer", passk_by_role.get(role)), ("first attempt", pass1_by_role.get(role))):
            if not evals:
                continue
            m = aggregate_detection_metrics(evals)
            lines.append(
                f"| {role} | {label} | {m['n_reps']} | {_fmt_ratio(m['detection_rate'])} | "
                f"{_fmt_ratio(m['avg_coverage'])} | {m['tp']} | {m['fp']} | {m['fn']} | "
                f"{_fmt_ratio(m['precision'])} | {_fmt_ratio(m['recall'])} | "
                f"{_fmt_ratio(m['f1'])} | {_fmt(m['alerts_per_tp'], 1)} |"
            )
    lines += [
        "",
        "**Legend**",
        "",
        "- `M1` = detection rate / avg coverage, `M2` = precision / recall / F1, "
        "`M3` = alerts/TP.",
        "- Unit of analysis is the CVE (docs/sgv_protocol/00_proposta_relatore.md §2): "
        "TP = matched CVEs, FN = missed CVEs, FP = findings that paired to no candidate "
        "CVE (includes genuine extra vulnerabilities with no catalogued CVE, not only "
        "false positives — see the unmatched-findings legend above).",
        "- `reps` = repetitions pooled into this row (across every task in scope, for "
        "pooled tables). Counts sum over all of them (unit = CVE × repetition): a CVE "
        "found in every repetition contributes one TP per repetition, and TP + FN = "
        "sum of each pooled repetition's target CVEs (single task: target CVEs × "
        "reps) — read TP against that ceiling, not against the number of distinct "
        "target CVEs.",
        "- `final answer` (the headline row) = evaluated against the final accepted "
        "answer, after every retry — the system as a black box; same numbers as the "
        "`matched`/`missed CVEs`/`unmatched findings` counts above. Formerly labelled "
        "`pass@k`.",
        "- `first attempt` = diagnostic counterfactual: same evaluation against the "
        "agent's *first* attempt only, as if the SGV/rubric retry loop didn't exist. "
        "Formerly labelled `pass@1`.",
        "- `detection rate` = share of repetitions (with at least one target CVE) where "
        "≥1 CVE was matched. `avg coverage` = mean matched/target CVEs per repetition.",
        "- `alerts/TP` (M3) = (TP+FP)/TP — how many findings a reviewer has to read for "
        "every true positive actually surfaced; lower is better (less noise per real "
        "vulnerability). `n/a` when TP = 0 (nothing to divide by).",
        "- A final-answer row with higher recall (or F1) than its first-attempt row is "
        "the retry loop actually finding more; if precision drops (or alerts/TP rises) "
        "at the same time, the extra findings came at a cost — read them together, not "
        "recall alone.",
        "- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.",
        "",
    ]
    return lines


def _build_cve_rep_matrix(roles: Dict[str, List[Dict[str, Any]]], heading: str = "###") -> List[str]:
    """CVE × repetition hit matrix on the final answer — makes visible at a
    glance whether the same CVEs are found/missed across repetitions (e.g. the
    task6 misses being always the same four), information otherwise
    reconstructable only by cross-reading each repetition's missed list. The
    per-rep FP row doubles as the stability read on the noise side."""
    from utils.cvss_eval import _candidate_cves

    by_role_task: Dict[Tuple[str, str], Dict[Any, Tuple[set, int]]] = {}
    for role, payloads in sorted(roles.items()):
        for p in payloads:
            ce = p.get("cvss_eval")
            if not isinstance(ce, dict):
                continue
            d = by_role_task.setdefault((role, p.get("task_id")), {})
            d[p.get("repetition")] = (
                {m.get("cve_id") for m in ce.get("matched", [])},
                ce.get("unmatched_findings", 0),
            )
    if not by_role_task:
        return []

    lines = [
        '<a id="cve-rep-matrix"></a>',
        f"{heading} CVE × repetition (final answer)",
        "",
        "_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings "
        "with no GT CVE in that repetition — the per-rep noise. A CVE row that is all "
        "✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling "
        "instability._",
        "",
    ]
    for (role, task_id), by_rep in sorted(by_role_task.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        candidates = _candidate_cves(task_id or "")
        reps = sorted(by_rep)
        header_reps = " | ".join(f"rep {r}" for r in reps)
        lines.append(f"| {task_id} — {role} | {header_reps} | hit rate |")
        lines.append("| --- |" + " --- |" * (len(reps) + 1))
        for cve in candidates:
            hits = [cve["id"] in by_rep[r][0] for r in reps]
            marks = " | ".join("✓" if h else "✗" for h in hits)
            lines.append(f"| {cve['id']} | {marks} | {sum(hits)}/{len(reps)} |")
        fp_cells = " | ".join(str(by_rep[r][1]) for r in reps)
        fp_total = sum(by_rep[r][1] for r in reps)
        lines.append(f"| unmatched (FP) | {fp_cells} | {fp_total} tot |")
        lines.append("")
    return lines


def _retry_cause(attempt: Dict[str, Any]) -> str:
    """Which gate triggered the retry *after* this attempt: the SGV gate runs
    first, so a failed SGV is the cause even when the rubric would also have
    failed; otherwise the retry belongs to the rubric judge. 'unknown' when
    the attempt carries neither signal (non-vuln tasks, older runs)."""
    sgv = attempt.get("sgv_eval")
    if isinstance(sgv, dict) and sgv.get("passed") is False:
        return "SGV"
    if attempt.get("verdict") is not None or attempt.get("judge_score") is not None:
        return "rubric"
    return "unknown"


def _build_retry_channel_section(roles: Dict[str, List[Dict[str, Any]]], heading: str = "###") -> List[str]:
    """Doc 07 variation 1 (agreed 2026-07-14): stratify the first-attempt →
    final-answer detection delta by *which* gate caused each retry (SGV vs
    rubric judge — two independent retry channels, 06_implementazione). Each
    attempt's cvss_estimate is saved in history, so the per-transition deltas
    are recomputed here deterministically (no LLM, no new runs): the TP/FP
    delta between attempt i and i+1 is attributed to the gate that rejected
    attempt i. Answers the proposal's §4 open question — is the perimeter
    widening due to the induced re-examination (and which one) or to sampling
    variability alone."""
    from utils.cvss_eval import evaluate_cvss_estimate

    stats: Dict[Tuple[str, str], Dict[str, int]] = {}
    for role, payloads in sorted(roles.items()):
        for p in payloads:
            history = p.get("history") or []
            if len(history) < 2 or not isinstance(p.get("cvss_eval"), dict):
                continue
            task_id = p.get("task_id") or ""
            evals = [evaluate_cvss_estimate(task_id, h.get("cvss_estimate")) for h in history]

            def _counts(e: Optional[Dict[str, Any]]) -> Tuple[int, int]:
                if not isinstance(e, dict):
                    return 0, 0
                return len(e.get("matched", [])), e.get("unmatched_findings", 0)

            for i in range(len(history) - 1):
                cause = _retry_cause(history[i])
                tp_prev, fp_prev = _counts(evals[i])
                tp_next, fp_next = _counts(evals[i + 1])
                s = stats.setdefault((role, cause), {"transitions": 0, "d_tp": 0, "d_fp": 0})
                s["transitions"] += 1
                s["d_tp"] += tp_next - tp_prev
                s["d_fp"] += fp_next - fp_prev
    if not stats:
        return []

    lines = [
        '<a id="retry-channel"></a>',
        f"{heading} Detection delta by retry channel (doc 07, variation 1)",
        "",
        "| role | retry cause | transitions | ΔTP | ΔFP |",
        "| --- | --- | --- | --- | --- |",
    ]
    for (role, cause), s in sorted(stats.items()):
        lines.append(
            f"| {role} | {cause} | {s['transitions']} | {s['d_tp']:+d} | {s['d_fp']:+d} |"
        )
    lines += [
        "",
        "**Legend**",
        "",
        "- Each retry transition (attempt i → i+1) is attributed to the gate that "
        "rejected attempt i: `SGV` when the syntactic verifier failed (it runs "
        "first), `rubric` when the SGV passed and the retry came from the judge, "
        "`unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/"
        "unmatched findings gained (+) or lost (−) across that transition, summed "
        "per channel.",
        "- The channel sums together equal the first-attempt → final-answer gap in "
        "the detection table above — this table splits that gap by cause "
        "(docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers "
        "the §4 open question of the proposal).",
        "- Positive ΔTP with small ΔFP = that channel's re-examination genuinely "
        "recovers vulnerabilities; ΔFP-only = that channel adds noise.",
        "",
    ]
    return lines


def _build_sgv_detection_cross_section(roles: Dict[str, List[Dict[str, Any]]], heading: str = "###") -> List[str]:
    """Doc 07 variation 2 (agreed 2026-07-14): cross M2 with Blocco C — do
    findings that are SGV-conform in the final answer have a higher TP rate
    than the ones the SGV let through non-conform after exhausting retries?
    Empirical evidence (without discarding anything) on whether the syntactic
    checks correlate with substantive correctness, i.e. whether the §4.5
    discard would be justified."""
    per_cell: Dict[Tuple[str, str], Dict[str, int]] = {}
    for role, payloads in sorted(roles.items()):
        for p in payloads:
            ce = p.get("cvss_eval")
            if not isinstance(ce, dict):
                continue
            history = p.get("history") or []
            sgv = (history[-1].get("sgv_eval") if history else None) or {}
            conform_by_fn = {
                _normalize_function_name(f.get("function")): f.get("passed")
                for f in sgv.get("per_finding", [])
                if isinstance(f, dict)
            }

            def _bucket(function: Any) -> str:
                passed = conform_by_fn.get(_normalize_function_name(function))
                if passed is True:
                    return "conform"
                if passed is False:
                    return "non-conform"
                return "no SGV record"

            for m in ce.get("matched", []):
                cell = per_cell.setdefault((role, _bucket(m.get("function"))), {"tp": 0, "fp": 0})
                cell["tp"] += 1
            for u in ce.get("unmatched", []):
                cell = per_cell.setdefault((role, _bucket(u.get("function"))), {"tp": 0, "fp": 0})
                cell["fp"] += 1
    if not per_cell:
        return []

    lines = [
        '<a id="sgv-detection-cross"></a>',
        f"{heading} Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)",
        "",
        "| role | SGV status (final answer) | TP | FP | precision |",
        "| --- | --- | --- | --- | --- |",
    ]
    order = {"conform": 0, "non-conform": 1, "no SGV record": 2}
    for (role, bucket), cell in sorted(per_cell.items(), key=lambda kv: (kv[0][0], order.get(kv[0][1], 9))):
        tp, fp = cell["tp"], cell["fp"]
        prec = _fmt_ratio(tp / (tp + fp)) if (tp + fp) else "n/a"
        lines.append(f"| {role} | {bucket} | {tp} | {fp} | {prec} |")
    lines += [
        "",
        "**Legend**",
        "",
        "- Findings of the final answer bucketed by their per-finding SGV outcome "
        "(G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the "
        "SGV let it through after exhausting retries (non-discard policy), `no SGV "
        "record` = the SGV reported nothing for that function name.",
        "- If `non-conform` precision is clearly lower than `conform`, the syntactic "
        "checks correlate with substantive correctness — first empirical evidence "
        "for (or against) the §4.5 discard, gathered without discarding anything "
        "(docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).",
        "- A table with only `conform` rows means every final finding passed the "
        "SGV in this run — no signal either way, not a confirmation.",
        "",
    ]
    return lines


def _build_severity_metrics_section(roles: Dict[str, List[Dict[str, Any]]], heading: str = "###") -> List[str]:
    """S1 (exact vector match) + S2 (per-metric accuracy/ordinal distance) +
    S3 (baseline: null model always guessing the modal GT vector), computed
    only on TP (matched findings) — docs/sgv_protocol/00_proposta_relatore.md
    §5.2, 07_metriche_M_S_2026-07-14.md. Unlike M1/M2/M3 this isn't split
    final answer/first attempt: severity is a downstream measurement on the
    final accepted answer only, not a property of the retry loop."""
    from utils.cvss_eval import EXPLOITABILITY_METRICS, IMPACT_METRICS, SUBSEQUENT_METRICS, aggregate_severity_metrics

    task_ids = sorted({p.get("task_id") for payloads in roles.values() for p in payloads if p.get("task_id")})
    if not task_ids:
        return []

    by_role = {}
    for role, payloads in sorted(roles.items()):
        evals = [p["cvss_eval"] for p in payloads if isinstance(p.get("cvss_eval"), dict)]
        if not evals:
            continue
        agg = aggregate_severity_metrics(task_ids, evals)
        if agg:
            by_role[role] = agg
    if not by_role:
        return []

    lines = [
        '<a id="severity-metrics"></a>',
        f"{heading} Severity (S1, S2, S3 — computed on TP only)",
        "",
        "| role | n (TP) | S1 exact match | S3 baseline exact match |",
        "| --- | --- | --- | --- |",
    ]
    for role, agg in by_role.items():
        lines.append(
            f"| {role} | {agg['n']} | {_fmt_ratio(agg['s1_exact_match'])} | "
            f"{_fmt_ratio(agg['s3_baseline_exact_match'])} |"
        )

    lines += ["", f"{heading}# S2 — per-metric accuracy (agent vs. baseline), ordinal distance", ""]
    metrics = EXPLOITABILITY_METRICS + IMPACT_METRICS + SUBSEQUENT_METRICS
    lines += [
        "| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for role, agg in by_role.items():
        for metric in metrics:
            pm = agg["per_metric"].get(metric)
            if not pm:
                continue
            baseline_acc = agg["s3_baseline_per_metric"].get(metric)
            lines.append(
                f"| {role} | {metric} | {pm['n']} | {_fmt_ratio(pm['accuracy'])} | "
                f"{_fmt_ratio(baseline_acc)} | {_fmt(pm['avg_distance'], 2)} |"
            )
    lines += [
        "",
        "**Legend**",
        "",
        "- `S1` = exact match of the whole vector, `S2` = per-metric accuracy / ordinal "
        "distance (table above), `S3` = null-model baseline both are read against.",
        "- Computed only on matched findings (TP) — unmatched findings and missed CVEs "
        "carry no severity comparison, per the proposal (§5.2).",
        "- When a repetition reports the same handler more than once, the finding "
        "paired to the CVE (whose vector S reads) is the first in agent output order "
        "— function name is the only identity available, and a GT-aware tie-break "
        "would bias S upward (see cvss_eval._match_finding). The duplicates are "
        "visible in the unmatched table via the shared `group` letter.",
        "- `S1 exact match` = share of TP findings whose *entire* estimated vector "
        "(8 base metrics, 11 when SC/SI/SA were emitted) matches the published one field "
        "for field.",
        "- `S3 baseline` = a null model that always guesses the modal vector among the "
        "target CVEs in scope (one task, or every task pooled together) — read "
        "S1/accuracy as a margin **above** this, not in absolute terms. With a single "
        "target CVE in scope the baseline degenerates to 100% by construction (the modal "
        "vector of one CVE is that CVE's own vector) — real property of the dataset, not "
        "a bug; the margin is only informative with several target CVEs with differing "
        "vectors in scope.",
        "- `avg ordinal distance` (0-1, 0 = identical, 1 = opposite ends of the scale) — "
        "severity-aware: a None→High miss is penalized more than a None→Low one.",
        "- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.",
        "",
    ]
    return lines


def _highlight_function(text: str, function: str) -> str:
    """Bold every occurrence of the function name so a reader scanning a
    multi-finding narrative can spot the passage about this one finding.
    Backtick-wrapped occurrences (`` `setCorsHeader` ``, the common case in
    these narratives) are bolded as a whole code span — bolding only the text
    *inside* backticks would be inert, Markdown doesn't parse emphasis inside
    a code span."""
    if not text or not function:
        return text
    escaped = re.escape(function)
    text = re.sub(rf"`{escaped}`", lambda m: f"**{m.group(0)}**", text, flags=re.IGNORECASE)
    text = re.sub(rf"(?<!`){escaped}(?!`)", lambda m: f"**{m.group(0)}**", text, flags=re.IGNORECASE)
    return text


def _normalize_function_name(function: Optional[str]) -> str:
    """Lowercase and strip trailing '(NF name)'/'(Cross-NF ...)' annotations the
    agent sometimes appends (e.g. 'setCorsHeader (PCF)' vs 'setCorsHeader') so
    the same function isn't treated as two different locations."""
    name = (function or "").strip().lower()
    while True:
        stripped = re.sub(r"\s*\([^()]*\)\s*$", "", name).strip()
        if stripped == name:
            return name
        name = stripped


def _letter_label(n: int) -> str:
    """0, 1, 2, ... -> 'a', 'b', ..., 'z', 'aa', 'ab', ... (spreadsheet-style)."""
    label = ""
    while True:
        label = chr(ord("a") + n % 26) + label
        n = n // 26 - 1
        if n < 0:
            return label


def _cluster_unmatched_findings(
    entries: List[Tuple[str, str, Any, Optional[str], Dict[str, Any], Dict[str, Any]]],
    semantic_check: bool = True,
) -> Tuple[List[int], set]:
    """Assign a cluster id to each unmatched finding so the same finding
    recurring across repetitions can be spotted at a glance, without hiding
    any row.

    Phase 1 (always, free): findings within the same (task_id, role) that
    share a normalized function name and an identical vector are the same
    finding re-reported — grouped with no LLM call.
    Phase 2 (if semantic_check): candidate groups that share a function but
    differ in vector are ambiguous (same bug re-estimated vs. two distinct
    bugs in the same function) — resolved with one LLM call per function,
    cached like the Blocco A consistency check.

    Returns (cluster_id per entry, set of cluster ids the LLM actually
    inspected and judged genuinely different — as opposed to never compared
    at all — so the caller can render the two "no group" cases differently).
    """
    cluster_id = [0] * len(entries)
    key_to_id: Dict[Tuple[str, str, str, str], int] = {}
    for idx, (role, task_id, _rep, _run_id, _final_answer, u) in enumerate(entries):
        function_norm = _normalize_function_name(u.get("function"))
        vector = (u.get("vector") or "").strip()
        key = (task_id, role, function_norm, vector)
        if key not in key_to_id:
            key_to_id[key] = len(key_to_id)
        cluster_id[idx] = key_to_id[key]

    if not semantic_check:
        return cluster_id, set()

    by_function: Dict[Tuple[str, str, str], List[Tuple[str, int]]] = {}
    for (task_id, role, function_norm, vector), cid in key_to_id.items():
        if not function_norm:
            continue
        by_function.setdefault((task_id, role, function_norm), []).append((vector, cid))
    ambiguous = {k: v for k, v in by_function.items() if len({c for _, c in v}) > 1}
    if not ambiguous:
        return cluster_id, set()

    from agents.judge_agent import run_semantic_equivalence_check
    from agents._llm_utils import resolve_model_config

    cache_path = Path(RESULTS_PATH) / "evaluation" / "semantic_cache.json"
    cache: Dict[str, Any] = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    if "semantic_check" not in config.MODELS:
        raise ValueError("MODELS['semantic_check'] must be set for semantic consistency checks")
    model, sem_is_hosted = resolve_model_config("semantic_check")
    base_url = config.OLLAMA_BASE_URL

    cache_updated = False
    remap: Dict[int, int] = {}
    checked_not_equal: set = set()
    for (task_id, role, function_norm), vector_clusters in ambiguous.items():
        distinct_vectors = sorted({v for v, _ in vector_clusters})
        descriptions = [
            f"Function `{function_norm}`, estimated CVSS vector `{v}`." for v in distinct_vectors
        ]
        check_id = f"unmatched/{task_id}/{role}/{function_norm}"
        cache_key = (
            check_id + "/" + hashlib.sha256(json.dumps(descriptions).encode()).hexdigest()[:16]
        )
        if cache_key in cache:
            result = cache[cache_key]
        else:
            result = run_semantic_equivalence_check(
                task_id=check_id,
                reasonings=descriptions,
                model=model,
                base_url=base_url,
                is_hosted=sem_is_hosted,
            )
            cache[cache_key] = result
            cache_updated = True
        if result.get("equivalent", False):
            target = min(cid for _, cid in vector_clusters)
            for _, cid in vector_clusters:
                if cid != target:
                    remap[cid] = target
        else:
            checked_not_equal.update(cid for _, cid in vector_clusters)

    if cache_updated:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")

    if remap:
        cluster_id = [remap.get(cid, cid) for cid in cluster_id]
        checked_not_equal = {remap.get(cid, cid) for cid in checked_not_equal}
    return cluster_id, checked_not_equal


def _compute_finding_groups(
    roles: Dict[str, List[Dict[str, Any]]], semantic_check: bool = True
) -> Tuple[Dict[Tuple[str, str, Any, str], str], Dict[Tuple[str, str, Any, int], str]]:
    """Recurrence labels shared between the matched (vector detail) and
    unmatched tables, so the same underlying finding carries the same letter
    wherever it appears (call 13 follow-up: an unmatched duplicate of an
    already-matched CVE was indistinguishable from a brand-new finding).

    Cluster seeds: every matched finding of the same (task, role, CVE) is the
    same vulnerability by definition — matching is per repetition, so a CVE
    found again in a later repetition is a new TP, not an unmatched. An
    unmatched finding joins a seed cluster when its function name matches one
    of that CVE's handler functions (same containment rule as
    cvss_eval._match_finding, deterministic, no LLM): that's the
    duplicate-within-a-repetition case, where the CVE was already consumed by
    an earlier finding of the same rep. Leftover unmatched findings are
    clustered among themselves as before (_cluster_unmatched_findings,
    incl. the cached LLM check for same-function/different-vector).

    Returns (matched_labels, unmatched_markers):
      matched_labels[(task_id, role, rep, cve_id)] = letter, only for
        clusters with >1 member (recurrence is the signal);
      unmatched_markers[(task_id, role, rep, idx)] = letter, '≠' or '—'
        (idx = position in that repetition's `unmatched` list).
    """
    from utils.cvss_eval import _candidate_cves

    matched_entries: List[Tuple[str, str, Any, str]] = []
    unmatched_entries: List[Tuple[str, str, Any, Optional[str], Dict[str, Any], Dict[str, Any], int]] = []
    for role, payloads in sorted(roles.items()):
        for p in payloads:
            ce = p.get("cvss_eval")
            if not isinstance(ce, dict):
                continue
            task_id, rep = p.get("task_id"), p.get("repetition")
            for m in ce.get("matched", []):
                matched_entries.append((task_id, role, rep, m.get("cve_id")))
            for idx, u in enumerate(ce.get("unmatched", [])):
                unmatched_entries.append((role, task_id, rep, p.get("run_id"), {}, u, idx))

    # Same triage order as the unmatched table, so letters follow reading order.
    unmatched_entries.sort(
        key=lambda e: e[5].get("computed_score_B", e[5].get("declared_score", -1.0)) or -1.0,
        reverse=True,
    )

    # Seed clusters: one per (task, role, CVE) with matched rows.
    cve_cluster: Dict[Tuple[str, str, str], int] = {}
    members: Dict[int, int] = {}
    matched_cids: List[int] = []
    for task_id, role, _rep, cve_id in matched_entries:
        cid = cve_cluster.setdefault((task_id, role, cve_id), len(cve_cluster))
        members[cid] = members.get(cid, 0) + 1
        matched_cids.append(cid)

    handlers_cache: Dict[str, List[Tuple[str, List[str]]]] = {}

    def _handlers(task_id: str) -> List[Tuple[str, List[str]]]:
        if task_id not in handlers_cache:
            handlers_cache[task_id] = [
                (cve["id"], [h.lower() for h in (cve.get("handler_functions") or [])])
                for cve in _candidate_cves(task_id)
            ]
        return handlers_cache[task_id]

    linked: Dict[int, int] = {}  # position in unmatched_entries -> cluster id
    leftover: List[Tuple[int, Tuple]] = []
    for pos, entry in enumerate(unmatched_entries):
        role, task_id, _rep, _run_id, _fa, u, _idx = entry
        function = str(u.get("function", "")).strip().lower()
        cid = None
        if function and task_id:
            for cve_id, handlers in _handlers(task_id):
                if any(h and (h in function or function in h) for h in handlers):
                    cid = cve_cluster.get((task_id, role, cve_id))
                    if cid is not None:
                        break
        if cid is None:
            leftover.append((pos, entry))
        else:
            linked[pos] = cid
            members[cid] = members.get(cid, 0) + 1

    offset = len(cve_cluster)
    leftover_cids, checked_not_equal = _cluster_unmatched_findings(
        [e[:6] for _, e in leftover], semantic_check=semantic_check
    )
    checked_not_equal = {cid + offset for cid in checked_not_equal}
    for (pos, _entry), cid in zip(leftover, leftover_cids):
        linked[pos] = cid + offset
        members[cid + offset] = members.get(cid + offset, 0) + 1

    # Letters in display order: matched section first, then unmatched triage order.
    labels: Dict[int, str] = {}

    def _label(cid: int) -> Optional[str]:
        if members.get(cid, 0) > 1 and cid not in labels:
            labels[cid] = _letter_label(len(labels))
        return labels.get(cid)

    matched_labels: Dict[Tuple[str, str, Any, str], str] = {}
    for (task_id, role, rep, cve_id), cid in zip(matched_entries, matched_cids):
        label = _label(cid)
        if label:
            matched_labels[(task_id, role, rep, cve_id)] = label

    unmatched_markers: Dict[Tuple[str, str, Any, int], str] = {}
    for pos, (role, task_id, rep, _run_id, _fa, _u, idx) in enumerate(unmatched_entries):
        cid = linked[pos]
        label = _label(cid)
        unmatched_markers[(task_id, role, rep, idx)] = label or (
            "≠" if cid in checked_not_equal else "—"
        )
    return matched_labels, unmatched_markers


def _final_answer_with_prompt(p: Dict[str, Any]) -> Dict[str, Any]:
    """final_answer as saved on disk is a whitelisted view (answer/reasoning/
    confidence/cvss_estimate only, utils/experiment_utils.py:_save_result:344)
    — prompt_system/prompt_user live on the full history entry instead
    (history is saved unfiltered). Merge them back in for display purposes."""
    final_answer = dict(p.get("final_answer") or {})
    history = p.get("history") or []
    if history and isinstance(history[-1], dict):
        last = history[-1]
        for key in ("prompt_system", "prompt_user"):
            if key in last:
                final_answer[key] = last[key]
    return final_answer


def _fence_for(text: str) -> str:
    """A backtick fence guaranteed not to be closed early by the content:
    task prompts embed their own ```go / ```md fenced blocks (the source
    excerpt, the output-format template), so a plain ``` fence gets closed
    by the first one it contains. Use one backtick longer than the longest
    run already in the text (minimum 3, per CommonMark)."""
    runs = re.findall(r"`+", text)
    longest = max((len(r) for r in runs), default=0)
    return "`" * max(3, longest + 1)


def _build_prompt_detail_block(final_answer: Dict[str, Any]) -> List[str]:
    """Collapsible section with the exact prompt sent to the LLM for this
    repetition (system + user, retry addendum included when present) —
    saved verbatim in the raw JSON (`final_answer.prompt_system/prompt_user`,
    utils/experiment_utils.py:_run_agent) but not otherwise visible outside
    it. Useful to check what the model actually saw, e.g. when diagnosing
    non-exhaustive analysis on long task_full files."""
    prompt_system = str(final_answer.get("prompt_system") or "").strip()
    prompt_user = str(final_answer.get("prompt_user") or "").strip()
    if not prompt_system and not prompt_user:
        return []
    lines = ["<details>", "<summary>Prompt sent to the model (system + user)</summary>", ""]
    if prompt_system:
        fence = _fence_for(prompt_system)
        lines += ["**System:**", "", fence, prompt_system, fence, ""]
    if prompt_user:
        fence = _fence_for(prompt_user)
        lines += ["**User:**", "", fence, prompt_user, fence, ""]
    lines += ["</details>", ""]
    return lines


def _write_unmatched_finding_file(
    path: Path,
    task_id: str,
    experiment_id: str,
    role: str,
    rep: Any,
    run_id: Optional[str],
    u: Dict[str, Any],
    final_answer: Dict[str, Any],
    group_label: Optional[str] = None,
) -> None:
    """One self-contained file per unmatched finding: its structured data plus
    the agent's full narrative for that repetition, so an expert triaging it
    doesn't have to open the raw multi-repetition JSON at all."""
    function = u.get("function") or "—"
    answer = _highlight_function(str(final_answer.get("answer") or "").strip(), function)
    reasoning = _highlight_function(str(final_answer.get("reasoning") or "").strip(), function)

    lines = [
        f"# Unmatched finding — {task_id} ({experiment_id}) — {role}, rep {rep}",
        "",
        "| field | value |",
        "| --- | --- |",
        f"| function | `{function}` |",
        f"| vector (estimated) | `{u.get('vector', '—')}` |",
        f"| score declared | {_fmt(u.get('declared_score'), 1)} |",
        f"| score computed (official CVSS 4.0 math) | {_fmt(u.get('computed_score_B'), 1)} |",
        f"| group (shared with matched table) | {group_label or '—'} |",
        "",
        "## Agent narrative for this repetition",
        "",
        f"_Shared across every finding reported in the same repetition — occurrences "
        f"of `{function}` are **bolded** below to help locate the relevant passage._",
        "",
    ]
    if answer:
        lines += ["**Answer:**", "", answer, ""]
    if reasoning:
        lines += ["**Reasoning:**", "", reasoning, ""]
    lines += _build_prompt_detail_block(final_answer)
    lines += [
        "---",
        f"_Source: `results/{task_id}/{experiment_id}/{role}/*.json`, run_id "
        f"`{run_id or 'legacy (no run_id)'}`, repetition {rep}._",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_matched_finding_file(
    path: Path,
    task_id: str,
    experiment_id: str,
    role: str,
    rep: Any,
    run_id: Optional[str],
    m: Dict[str, Any],
    final_answer: Dict[str, Any],
    group_label: Optional[str] = None,
) -> None:
    """One self-contained file per finding that DID pair to a ground-truth
    CVE: its structured data plus the agent's full narrative for that
    repetition. Mirrors _write_unmatched_finding_file — the vector-detail
    table shows the field-by-field diff, this shows *why* the agent estimated
    it that way (or misdiagnosed the root cause) without opening the raw
    multi-repetition JSON."""
    function = m.get("function") or "—"
    answer = _highlight_function(str(final_answer.get("answer") or "").strip(), function)
    reasoning = _highlight_function(str(final_answer.get("reasoning") or "").strip(), function)

    lines = [
        f"# Matched finding — {m.get('cve_id', '—')} — {task_id} ({experiment_id}) — {role}, rep {rep}",
        "",
        "| field | value |",
        "| --- | --- |",
        f"| GT CVE | {m.get('cve_id', '—')} |",
        f"| group (shared with unmatched table) | {group_label or '—'} |",
        f"| function | `{function}` |",
        f"| vector (estimated) | `{m.get('estimated_vector', '—')}` |",
        f"| vector (published) | `{m.get('published_vector', '—')}` |",
        f"| score computed (official CVSS 4.0 math) | {_fmt(m.get('computed_score_B'), 1)} |",
        f"| score published | {_fmt(m.get('published_score'), 1)} |",
        "",
        "## Agent narrative for this repetition",
        "",
        f"_Shared across every finding reported in the same repetition — occurrences "
        f"of `{function}` are **bolded** below to help locate the relevant passage._",
        "",
    ]
    if answer:
        lines += ["**Answer:**", "", answer, ""]
    if reasoning:
        lines += ["**Reasoning:**", "", reasoning, ""]
    lines += _build_prompt_detail_block(final_answer)
    lines += [
        "---",
        f"_Source: `results/{task_id}/{experiment_id}/{role}/*.json`, run_id "
        f"`{run_id or 'legacy (no run_id)'}`, repetition {rep}._",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _build_cvss_unmatched(
    roles: Dict[str, List[Dict[str, Any]]],
    experiment_id: str,
    results_path: str,
    unmatched_markers: Optional[Dict[Tuple[str, str, Any, int], str]] = None,
) -> List[str]:
    """Findings with no ground-truth CVE, ranked most-severe-first by the
    officially recomputed score — the experts' use case: potential
    vulnerabilities not (yet) tied to a CVE, ready for manual triage. Each row
    also gets a self-contained detail file (see _write_unmatched_finding_file)
    since the finding record itself carries no free-text rationale.

    Every repetition's finding stays its own row (nothing is deduplicated or
    hidden) — the `group` column only adds a recurrence label, shared with the
    vector-detail (matched) section so an unmatched duplicate of an
    already-matched CVE carries the CVE's same letter (see
    _compute_finding_groups)."""
    entries = []
    for role, payloads in sorted(roles.items()):
        for p in payloads:
            ce = p.get("cvss_eval")
            if not isinstance(ce, dict):
                continue
            final_answer = _final_answer_with_prompt(p)
            for idx, u in enumerate(ce.get("unmatched", [])):
                entries.append(
                    (role, p.get("task_id"), p.get("repetition"), p.get("run_id"), final_answer, u, idx)
                )
    if not entries:
        return []

    entries.sort(
        key=lambda e: e[5].get("computed_score_B", e[5].get("declared_score", -1.0)) or -1.0,
        reverse=True,
    )

    if unmatched_markers is None:
        _, unmatched_markers = _compute_finding_groups(roles)

    out_dir = Path(results_path) / "evaluation" / "unmatched_findings"
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        '<a id="unmatched-findings"></a>',
        "### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)",
        "",
        "| # | group | details | score (from vector) | declared | function | task | role | rep | vector |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    seen: Dict[Tuple[str, str, Any], int] = {}
    for i, (role, task_id, rep, run_id, final_answer, u, idx) in enumerate(entries, 1):
        key = (task_id, role, rep)
        seen[key] = seen.get(key, 0) + 1
        filename = f"{task_id}_{experiment_id}_{role}_rep{rep}_f{seen[key]}.md"
        marker = unmatched_markers.get((task_id, role, rep, idx), "—")
        _write_unmatched_finding_file(
            out_dir / filename, task_id, experiment_id, role, rep, run_id, u, final_answer,
            group_label=marker,
        )
        lines.append(
            f"| {i} | {marker} | [detail](unmatched_findings/{filename}) | "
            f"{_fmt(u.get('computed_score_B'), 1)} | {_fmt(u.get('declared_score'), 1)} | "
            f"`{u.get('function') or '—'}` | {task_id} | {role} | {rep} | `{u.get('vector', '—')}` |"
        )
    lines += [
        "",
        "**Legend**",
        "",
        "- One row per finding the agent reported that matched no ground-truth CVE — "
        "either a false positive, or a genuine extra vulnerability with no catalogued "
        "CVE. Never counted against the evaluation (design choice: this is the "
        "practical use case, findings worth a human's triage).",
        "- `group` = a letter (a, b, c…) means same-letter rows recur. **Letters are "
        "shared with the vector-detail section above**: an unmatched row carrying "
        "the same letter as a matched CVE sits on one of that CVE's handler "
        "functions (the CVE was already consumed in that repetition) — the same "
        "*location identity* the ground truth itself uses, so it is a **probable "
        "duplicate** of the matched CVE, not verified semantically: a handler can "
        "host more than one distinct bug, so in triage treat it as a duplicate to "
        "confirm quickly, not as a new candidate to score. Letters on "
        "unmatched-only clusters mean same function + identical vector (or an "
        "LLM-confirmed equivalent one). `≠` means the function recurred with a "
        "different vector and the LLM judged it a genuinely different finding, not "
        "a re-estimate. `—` means the function was seen only once — nothing to "
        "compare, no LLM call made. Grouping never removes or merges rows, it only "
        "labels them.",
        "- `score (from vector)` = the recomputed score, official CVSS 4.0 math — sort "
        "key, most severe first.",
        "- `declared` = the score the agent stated directly; diagnostic only (see note "
        "above, not produced from the vector).",
        "- `function` = the Go function the agent pointed to as the vulnerability's "
        "location.",
        "- `task` / `role` = which task and role produced this finding.",
        "- `rep` = repetition index (1-based) — which run of that task/role produced "
        "this finding.",
        "- `vector` = the full CVSS 4.0 vector string the agent estimated.",
        "- `details` = link to a self-contained file with this finding's structured "
        "data plus the agent's full narrative for that repetition (function name "
        "bolded for quick scanning) — everything needed to review it without opening "
        "the raw JSON.",
        "",
    ]
    return lines


def _build_cvss_vector_detail(
    roles: Dict[str, List[Dict[str, Any]]],
    experiment_id: str,
    results_path: str,
    matched_labels: Optional[Dict[Tuple[str, str, Any, str], str]] = None,
) -> List[str]:
    """Per-finding estimated vs. published CVSS vector, one compact table per
    CVE: rows are the compared metrics (labelled with the full name from the
    dataset legend), columns are estimated/published — a diverging field is
    then visible at a glance without recomputing it from the aggregate
    bands/matches above. Each table also gets a self-contained detail file
    (see _write_matched_finding_file) with the agent's full reasoning for
    that repetition, linked right below — mirrors the unmatched-findings
    table so matched CVEs aren't the only ones without visible rationale."""
    from utils.cvss_eval import (
        _parse_vector,
        EXPLOITABILITY_METRICS,
        IMPACT_METRICS,
        SUBSEQUENT_METRICS,
        load_cvss_dataset,
    )

    entries = []
    for role, payloads in sorted(roles.items()):
        for p in payloads:
            ce = p.get("cvss_eval")
            if not isinstance(ce, dict):
                continue
            for m in ce.get("matched", []):
                if "estimated_vector" not in m:
                    continue
                entries.append(
                    (role, p.get("task_id"), p.get("repetition"), p.get("run_id"),
                     _final_answer_with_prompt(p), m)
                )
    if not entries:
        return []

    legend = load_cvss_dataset().get("_meta", {}).get("legenda_metriche", {})
    metrics = EXPLOITABILITY_METRICS + IMPACT_METRICS

    out_dir = Path(results_path) / "evaluation" / "matched_findings"
    out_dir.mkdir(parents=True, exist_ok=True)

    if matched_labels is None:
        matched_labels, _ = _compute_finding_groups(roles)

    lines = [
        '<a id="vector-detail"></a>',
        "### Vector detail (estimated vs. published)",
        "",
        "_`group` letter (when present) = this CVE recurs — same letter on other "
        "matched reps and/or on rows of the unmatched table below (there it marks a "
        "finding on one of this CVE's handler functions: a probable duplicate to "
        "confirm in triage, not necessarily the same bug — see the unmatched "
        "legend)._",
        "",
    ]
    for role, task_id, rep, run_id, final_answer, m in entries:
        est = _parse_vector(m["estimated_vector"])
        pub = _parse_vector(m.get("published_vector") or "")
        group_label = matched_labels.get((task_id, role, rep, m.get("cve_id")))
        group_suffix = f" — group {group_label}" if group_label else ""
        lines.append(f"| **{m['cve_id']}** — {role}, rep {rep}{group_suffix} | estimated | published |")
        lines.append("|---|---|---|")
        # SC/SI/SA rows only when the agent emitted them (requested since 2026-07-10).
        shown_metrics = metrics + [c for c in SUBSEQUENT_METRICS if c in est]
        for code in shown_metrics:
            label = f"{code} — {legend.get(code, {}).get('name', code)}"
            e_val, p_val = est.get(code, "-"), pub.get(code, "-")
            if e_val != p_val:
                e_val, p_val = f"**{e_val}**", f"**{p_val}**"
            lines.append(f"| {label} | {e_val} | {p_val} |")
        if isinstance(m.get("computed_score_B"), (int, float)):
            declared = m.get("estimated_score", "-")
            lines.append(
                f"| base score — declared / from vector (official math) | "
                f"{declared} / **{m['computed_score_B']}** | {m.get('published_score', '-')} |"
            )
        filename = f"{task_id}_{experiment_id}_{role}_rep{rep}_{m['cve_id']}.md"
        _write_matched_finding_file(
            out_dir / filename, task_id, experiment_id, role, rep, run_id, m, final_answer,
            group_label=group_label,
        )
        lines.append(f"| [reasoning detail](matched_findings/{filename}) | | |")
        lines.append("")
    return lines


def _build_run_id_note(all_payloads: List[Dict[str, Any]]) -> List[str]:
    """One line per (role, run_id) contributing to this report — so a reader
    can tell straight from the file which run(s) it aggregates, without
    cross-checking folder names or timestamps by hand (the doc-07 problem)."""
    per_role_runs: Dict[str, set] = {}
    for p in all_payloads:
        per_role_runs.setdefault(p.get("_role", "?"), set()).add(p.get("run_id") or "legacy (no run_id)")
    lines = ["> **Run(s) in this report:**"]
    for role, runs in sorted(per_role_runs.items()):
        lines.append(f"> - `{role}`: {', '.join(sorted(runs))}")
    lines.append("")
    return lines


def _build_experiment_report(
    experiment_id: str,
    roles: Dict[str, List[Dict[str, Any]]],
    task_filter: Optional[List[str]] = None,
    per_task_id: Optional[str] = None,
    results_path: str = RESULTS_PATH,
) -> str:
    """Generate evaluation report.

    Args:
        experiment_id: 1A or 1B
        roles: dict of {role: [payloads]}
        task_filter: optional list of task_ids to include (None = all)
        per_task_id: if set, generate report for only this task_id; else aggregate
        results_path: where to write companion files (e.g. unmatched-finding detail pages)
    """
    lines = [f"# Evaluation Report: {experiment_id}", ""]

    all_payloads = [{"_role": role, **p} for role, payloads in roles.items() for p in payloads]

    if task_filter is not None:
        all_payloads = [p for p in all_payloads if p.get("task_id") in task_filter]
    
    if per_task_id is not None:
        all_payloads = [p for p in all_payloads if p.get("task_id") == per_task_id]
        lines[0] = f"# {experiment_id} — {per_task_id}"

    if not all_payloads:
        lines.append("No results found.")
        return "\n".join(lines) + "\n"

    lines += _build_run_id_note(all_payloads)

    total = len(all_payloads)
    correct = sum(1 for p in all_payloads if p.get("verdict") == "correct")
    wrong_list = [p for p in all_payloads if p.get("verdict") != "correct"]
    retried_list = [p for p in all_payloads if p.get("attempts", 1) > 1]
    inconsistency_task_filter = [per_task_id] if per_task_id is not None else task_filter
    inconsistencies, n_surface_equiv = _detect_inconsistencies(roles, task_filter=inconsistency_task_filter)

    anomaly_count = len(wrong_list) + len(retried_list) + len(inconsistencies)

    summary_section = [
        '<a id="rubric-summary"></a>',
        "### Summary",
        "",
        "| metric | value |",
        "| --- | --- |",
        f"| total results | {total} |",
        f"| correct | {correct} ({_fmt_ratio(correct / total if total else None)}) |",
        f"| wrong | {len(wrong_list)} |",
        f"| retried (attempts > 1) | {len(retried_list)} |",
        f"| truly inconsistent tasks | {len(inconsistencies)} |",
        f"| surface-only differences (semantically equiv.) | {n_surface_equiv} |",
        "",
        "**Legend**",
        "",
        "- `truly inconsistent` = LLM confirmed different conclusions across repetitions.",
        "- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).",
        "",
    ]

    if anomaly_count == 0:
        summary_section.append("All tasks passed with full consistency — no anomalies detected.")
        summary_section.append("")
        anomalies_section = []
    else:
        anomalies_section = ['<a id="rubric-anomalies"></a>', "### Anomalies", ""]

        if wrong_list:
            anomalies_section += [f"#### Wrong verdicts ({len(wrong_list)})", ""]
            anomalies_section += [
                "| role | task_id | rep | attempts | confidence | score/delta |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
            for p in wrong_list:
                fa = p.get("final_answer", {})
                conf = fa.get("confidence") if isinstance(fa, dict) else None
                js = p.get("judge_score", {})
                score_info = js.get("total_score", js.get("delta", "n/a"))
                anomalies_section.append(
                    f"| {p['_role']} | {p.get('task_id')} | {p.get('repetition')} | "
                    f"{p.get('attempts')} | {_fmt(float(conf), 3) if isinstance(conf, (int, float)) else 'n/a'} "
                    f"| {score_info} |"
                )
            anomalies_section += [
                "",
                "**Legend**",
                "",
                "- `rep` = repetition index (1-based).",
                "- `attempts` = total LLM calls (all failed).",
                "- `confidence` = agent self-reported confidence on the final answer.",
                "- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).",
                "",
            ]

        if retried_list:
            anomalies_section += [f"#### Retries triggered ({len(retried_list)})", ""]
            anomalies_section += [
                "| role | task_id | rep | attempts | final_verdict |",
                "| --- | --- | --- | --- | --- |",
            ]
            for p in retried_list:
                anomalies_section.append(
                    f"| {p['_role']} | {p.get('task_id')} | {p.get('repetition')} | "
                    f"{p.get('attempts')} | {p.get('verdict')} |"
                )
            anomalies_section += [
                "",
                "**Legend**",
                "",
                "- Each row is one repetition.",
                "- `rep` = repetition index (1-based).",
                "- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).",
                "- `final_verdict` = outcome after all attempts.",
                "",
            ]

        if inconsistencies:
            anomalies_section += [f"#### Truly inconsistent reasoning ({len(inconsistencies)})", ""]
            for role, task_id, rep_reasonings, explanation in inconsistencies:
                anomalies_section.append(f"**{role} — {task_id}**")
                if explanation:
                    anomalies_section.append(f"> {explanation}")
                anomalies_section.append("")
                for rep, reasoning in rep_reasonings:
                    anomalies_section.append(f"**rep {rep}:**")
                    anomalies_section.append("")
                    anomalies_section.append(reasoning.strip())
                    anomalies_section.append("")
                anomalies_section.append("")

    # Rebuild roles dict with filtered payloads
    filtered_roles = {}
    for role in roles.keys():
        filtered_roles[role] = [p for p in all_payloads if p.get("_role") == role]

    # Block order (2026-07-16 feedback): Blocco B (deterministic CVSS metrics)
    # leads the report, Blocco C (SGV) follows, Blocco A (LLM-judge rubric:
    # summary/scores/anomalies) closes — each separated by a horizontal rule.
    # Within Blocco B, the concrete per-finding detail (vector detail vs GT,
    # then unmatched findings) comes before the aggregate roll-up tables: a
    # reader calibrates on "is this agent talking sense" from the detail
    # first, then uses the aggregates for a global summary — not the other
    # way around (2026-07-13 feedback).
    sgv_lines = _build_sgv_section(all_payloads)
    cvss_lines = _build_cvss_section(filtered_roles, experiment_id, results_path)

    toc = ['<a id="toc"></a>', "**Contents**", ""]
    if '<a id="vector-detail"></a>' in cvss_lines:
        toc.append("- [Vector detail (estimated vs. published)](#vector-detail)")
    if '<a id="unmatched-findings"></a>' in cvss_lines:
        toc.append("- [Unmatched findings](#unmatched-findings)")
    if '<a id="metrics-across-reps"></a>' in cvss_lines:
        toc.append("- [Metrics across repetitions](#metrics-across-reps)")
    if '<a id="detection-metrics"></a>' in cvss_lines:
        toc.append("  - [Detection (M1, M2, M3 — final answer vs first attempt)](#detection-metrics)")
    if '<a id="cve-rep-matrix"></a>' in cvss_lines:
        toc.append("  - [CVE × repetition](#cve-rep-matrix)")
    if '<a id="retry-channel"></a>' in cvss_lines:
        toc.append("  - [Detection delta by retry channel](#retry-channel)")
    if '<a id="sgv-detection-cross"></a>' in cvss_lines:
        toc.append("  - [Detection × SGV conformity](#sgv-detection-cross)")
    if '<a id="severity-metrics"></a>' in cvss_lines:
        toc.append("  - [Severity (S1, S2, S3)](#severity-metrics)")
    if '<a id="legacy-diagnostics"></a>' in cvss_lines:
        toc.append("  - [Legacy diagnostics (runs 1–3 comparability)](#legacy-diagnostics)")
    if sgv_lines:
        toc.append("- [SGV — Syntactic Grounding Verifier](#sgv)")
    toc.append("- [Rubric evaluation](#rubric-evaluation)")
    toc.append("  - [Summary](#rubric-summary)")
    toc.append("  - [Scores by role](#rubric-scores)")
    cost_lines = _build_cost_metrics_section(filtered_roles)
    if cost_lines:
        toc.append("  - [Cost (M5)](#cost-metrics)")
    if anomalies_section:
        toc.append("  - [Anomalies](#rubric-anomalies)")
    toc.append("")
    lines += toc

    lines += cvss_lines
    if sgv_lines:
        lines += ["", "---", ""]
        lines += sgv_lines
    lines += ["", "---", ""]
    lines += ['<a id="rubric-evaluation"></a>', "## Rubric evaluation (Blocco A, LLM judge)", ""]
    lines += summary_section
    lines += _build_scores_table(filtered_roles)
    lines.append("")
    lines += cost_lines
    lines += anomalies_section
    return "\n".join(lines) + "\n"


def _write_evaluation_reports(
    results_path: str,
    task_filter: Optional[List[str]] = None,
    experiment_ids: Optional[List[str]] = None,
    run_id: Optional[str] = None,
) -> None:
    data = _collect_results(results_path, run_id=run_id)
    eval_dir = Path(results_path) / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    ids_to_report = experiment_ids if experiment_ids else ["1A", "1B"]
    for experiment_id in ids_to_report:
        roles = data.get(experiment_id, {})
        n_results = sum(len(v) for v in roles.values())
        logger.info(
            "Report %s | %d result(s) across roles: %s",
            experiment_id,
            n_results,
            ", ".join(sorted(roles)) or "none",
        )

        all_payloads = [p for payloads in roles.values() for p in payloads]
        if task_filter is not None:
            all_payloads = [p for p in all_payloads if p.get("task_id") in task_filter]

        task_ids = sorted(set(p.get("task_id") for p in all_payloads if p.get("task_id")))
        for task_id in task_ids:
            task_report = _build_experiment_report(
                experiment_id, roles, task_filter=task_filter, per_task_id=task_id, results_path=results_path
            )
            filename = f"result_{task_id}_{experiment_id}.md"
            (eval_dir / filename).write_text(task_report, encoding="utf-8")
            logger.info("Written %s", filename)

    # Comparison report — only meaningful when both 1A and 1B are in scope
    if "1A" in ids_to_report and "1B" in ids_to_report:
        all_payloads_both = [
            {"_role": role, **p}
            for exp_id in ("1A", "1B")
            for role, payloads in data.get(exp_id, {}).items()
            for p in payloads
        ]
        lines = ["# Comparison 1A vs 1B", ""]
        lines += _build_run_id_note(all_payloads_both)
        lines += [
            "| role | accuracy_1A | accuracy_1B | delta |",
            "| --- | --- | --- | --- |",
        ]
        has_delta = False
        roles_present = sorted(set(data.get("1A", {})) | set(data.get("1B", {})))
        for role in roles_present:
            payloads_1a = data.get("1A", {}).get(role, [])
            payloads_1b = data.get("1B", {}).get(role, [])
            acc_1a = (sum(1 for p in payloads_1a if p.get("verdict") == "correct") / len(payloads_1a)) if payloads_1a else None
            acc_1b = (sum(1 for p in payloads_1b if p.get("verdict") == "correct") / len(payloads_1b)) if payloads_1b else None
            delta = (acc_1b - acc_1a) if acc_1a is not None and acc_1b is not None else None
            if delta and abs(delta) > 0:
                has_delta = True
            lines.append(
                f"| {role} | {_fmt_ratio(acc_1a)} | {_fmt_ratio(acc_1b)} | {_fmt_delta(delta)} |"
            )
        lines.append("")
        if not has_delta:
            lines.append("No accuracy difference between 1A and 1B.")

        # Pooled M1-M3/S1-S3/M5 across every task the role ran, per experiment
        # (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md) — same section
        # builders as the per-task reports, just fed the unfiltered roles dict
        # for each experiment instead of one task's payloads. Per-task numbers
        # are noisy with n=3 reps and few CVEs per task (e.g. S3 baseline
        # degenerates to 100% on single-CVE tasks); pooling across all vuln
        # tasks gives the statistically meaningful headline number.
        for exp_id in ("1A", "1B"):
            exp_roles = data.get(exp_id, {})
            if task_filter is not None:
                exp_roles = {
                    role: [p for p in payloads if p.get("task_id") in task_filter]
                    for role, payloads in exp_roles.items()
                }
            section_lines = (
                _build_detection_metrics_section(exp_roles)
                + _build_cve_rep_matrix(exp_roles)
                + _build_retry_channel_section(exp_roles)
                + _build_sgv_detection_cross_section(exp_roles)
                + _build_severity_metrics_section(exp_roles)
                + _build_cost_metrics_section(exp_roles)
            )
            if section_lines:
                lines += ["", f"## {exp_id} — pooled across all tasks", ""]
                lines += section_lines

        (eval_dir / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse
    import os

    from dotenv import load_dotenv

    load_dotenv()  # report regeneration may call the hosted semantic-check LLM
    # config reads the key at import time (before load_dotenv here): refresh it.
    config.OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    parser = argparse.ArgumentParser(
        description="List saved run_ids, or regenerate reports scoped to one run_id — "
        "the fix for 'which folder is which run': every repetition is tagged with the "
        "run_id of the main.py invocation that produced it, independent of folder naming."
    )
    parser.add_argument(
        "--list-runs", action="store_true",
        help="Print every (task, experiment, role, run_id) group with rep count and earliest timestamp.",
    )
    parser.add_argument(
        "--run-id", default=None,
        help="Regenerate result_*.md/comparison.md using only repetitions tagged with this run_id.",
    )
    args = parser.parse_args()

    if args.list_runs:
        rows = list_runs(RESULTS_PATH)
        if not rows:
            print("No results found.")
        else:
            print(f"{'task':24} {'exp':6} {'role':14} {'run_id':22} {'n':>3}  earliest")
            for task, exp, role, run, n, earliest in rows:
                print(f"{task:24} {exp:6} {role:14} {run:22} {n:>3}  {earliest}")
    elif args.run_id:
        _write_evaluation_reports(RESULTS_PATH, run_id=args.run_id)
        logger.info("Reports regenerated for run_id=%s", args.run_id)
    else:
        # No filter: regenerate every result_*.md/comparison.md from all saved
        # results, same as main.py does automatically at the end of a run.
        _write_evaluation_reports(RESULTS_PATH)
        logger.info("Reports regenerated for all results")
