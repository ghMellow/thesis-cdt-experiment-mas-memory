"""Evaluation report helpers — anomaly-focused output."""

import hashlib
import json
import logging
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


def _collect_results(results_path: str) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    base = Path(results_path)
    data: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    if not base.exists():
        return data
    for experiment_dir in sorted(p for p in base.iterdir() if p.is_dir() and p.name != "evaluation"):
        experiment_id = experiment_dir.name
        data.setdefault(experiment_id, {})
        for role_dir in sorted(p for p in experiment_dir.iterdir() if p.is_dir()):
            role = role_dir.name
            result_files = sorted(
                f for f in role_dir.glob("*.json") if not f.name.endswith("_solution.json")
            )
            data[experiment_id][role] = [json.loads(f.read_text(encoding="utf-8")) for f in result_files]
    return data


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
) -> Tuple[List[Tuple[str, str, List[Tuple[int, str]], str]], int]:
    """Detect tasks with inconsistent reasoning across repetitions.

    Phase 1 (always): string equality filter — fast, catches all surface differences.
    Phase 2 (if semantic_check=True): LLM confirms whether flagged items are truly
    semantically different or just paraphrases.

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

    cache_path = Path(RESULTS_PATH) / "evaluation" / "semantic_cache.json"
    cache: Dict[str, Any] = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    model = config.MODELS.get("semantic_check")
    if not model:
        raise ValueError("MODELS['semantic_check'] must be set for semantic consistency checks")
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
            )
            cache[cache_key] = result
            cache_updated = True

        verdict = "equiv" if result.get("equivalent", False) else "differ"
        logger.info("  → %s", verdict)
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
    lines = [
        "## Scores by role",
        "",
        "| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_math_delta | avg_textual_norm |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
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
        "| `brier_score` | all | mean((confidence − is\\_correct)²) — lower = better calibration; 0 = perfect, 0.25 = random |",
        "| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |",
        "| `avg_math_delta` | math | mean \\|answer − ground\\_truth\\| on math tasks — lower = more precise |",
        "| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |",
    ]
    return lines


def _build_experiment_report(experiment_id: str, roles: Dict[str, List[Dict[str, Any]]]) -> str:
    lines = [f"# Evaluation Report: {experiment_id}", ""]

    all_payloads = [{"_role": role, **p} for role, payloads in roles.items() for p in payloads]

    if not all_payloads:
        lines.append("No results found.")
        return "\n".join(lines) + "\n"

    total = len(all_payloads)
    correct = sum(1 for p in all_payloads if p.get("verdict") == "correct")
    wrong_list = [p for p in all_payloads if p.get("verdict") != "correct"]
    retried_list = [p for p in all_payloads if p.get("attempts", 1) > 1]
    inconsistencies, n_surface_equiv = _detect_inconsistencies(roles)

    anomaly_count = len(wrong_list) + len(retried_list) + len(inconsistencies)

    lines += [
        "## Summary",
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
        "_truly inconsistent_: LLM confirmed different conclusions across repetitions. "
        "_surface-only_: string-different but semantically equivalent (paraphrases, same logic).",
        "",
    ]

    if anomaly_count == 0:
        lines.append("All tasks passed with full consistency — no anomalies detected.")
        lines.append("")
    else:
        lines += ["## Anomalies", ""]

        if wrong_list:
            lines += [f"### Wrong verdicts ({len(wrong_list)})", ""]
            lines += [
                "| role | task_id | rep | attempts | confidence | score/delta |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
            for p in wrong_list:
                fa = p.get("final_answer", {})
                conf = fa.get("confidence") if isinstance(fa, dict) else None
                js = p.get("judge_score", {})
                score_info = js.get("total_score", js.get("delta", "n/a"))
                lines.append(
                    f"| {p['_role']} | {p.get('task_id')} | {p.get('repetition')} | "
                    f"{p.get('attempts')} | {_fmt(float(conf), 3) if isinstance(conf, (int, float)) else 'n/a'} "
                    f"| {score_info} |"
                )
            lines.append("")

        if retried_list:
            lines += [f"### Retries triggered ({len(retried_list)})", ""]
            lines += [
                "| role | task_id | rep | attempts | final_verdict |",
                "| --- | --- | --- | --- | --- |",
            ]
            for p in retried_list:
                lines.append(
                    f"| {p['_role']} | {p.get('task_id')} | {p.get('repetition')} | "
                    f"{p.get('attempts')} | {p.get('verdict')} |"
                )
            lines.append("")

        if inconsistencies:
            lines += [f"### Truly inconsistent reasoning ({len(inconsistencies)})", ""]
            for role, task_id, rep_reasonings, explanation in inconsistencies:
                lines.append(f"**{role} — {task_id}**")
                if explanation:
                    lines.append(f"> {explanation}")
                lines.append("")
                for rep, reasoning in rep_reasonings:
                    lines.append(f"- **rep {rep}:** {reasoning.replace(chr(10), ' ')}")
                    lines.append("")
                lines.append("")

    lines += _build_scores_table(roles)
    lines.append("")
    return "\n".join(lines) + "\n"


def _write_evaluation_reports(results_path: str) -> None:
    data = _collect_results(results_path)
    eval_dir = Path(results_path) / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    for experiment_id in ["1A", "1B"]:
        roles = data.get(experiment_id, {})
        n_results = sum(len(v) for v in roles.values())
        logger.info(
            "Report %s | %d result(s) across roles: %s",
            experiment_id,
            n_results,
            ", ".join(sorted(roles)) or "none",
        )
        report = _build_experiment_report(experiment_id, roles)
        (eval_dir / f"scores_{experiment_id}.md").write_text(report, encoding="utf-8")
        logger.info("Written scores_%s.md", experiment_id)

    # Comparison report
    lines = [
        "# Comparison 1A vs 1B",
        "",
        "| role | accuracy_1A | accuracy_1B | delta |",
        "| --- | --- | --- | --- |",
    ]
    has_delta = False
    for role in ["expert", "beginner"]:
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
    (eval_dir / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
