"""Evaluation report helpers — anomaly-focused output."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from config import RESULTS_PATH


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
    roles: Dict[str, List[Dict[str, Any]]]
) -> List[Tuple[str, str, List[Tuple[int, str]]]]:
    """Return (role, task_id, [(rep, reasoning), ...]) for tasks with inconsistent reasoning."""
    found = []
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
            unique = {r for _, r in rep_reasonings}
            if len(unique) > 1:
                found.append((role, task_id, rep_reasonings))
    return found


def _build_scores_table(roles: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    lines = [
        "## Scores by role",
        "",
        "| role | accuracy | avg_confidence | avg_attempts | avg_textual_norm | avg_math_delta |",
        "| --- | --- | --- | --- | --- | --- |",
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
        # normalized_score ∈ [0,1] enables cross-task comparison; fall back to raw/total_max
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
            f"{_fmt(_avg(confidences), 3)} | {_fmt(avg_attempts, 2)} | "
            f"{_fmt(_avg(textual_norms), 3)} | {_fmt(_avg(math_deltas), 3)} |"
        )
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
    inconsistencies = _detect_inconsistencies(roles)

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
        f"| inconsistent tasks | {len(inconsistencies)} |",
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
            lines += [f"### Inconsistent reasoning across repetitions ({len(inconsistencies)})", ""]
            for role, task_id, rep_reasonings in inconsistencies:
                lines.append(f"**{role} — {task_id}**")
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
        report = _build_experiment_report(experiment_id, data.get(experiment_id, {}))
        (eval_dir / f"scores_{experiment_id}.md").write_text(report, encoding="utf-8")

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
