"""Evaluation report helpers."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import RESULTS_PATH


def _record_consistency_finding(lines: List[str]) -> None:
    if not lines:
        return
    eval_path = Path(RESULTS_PATH) / "evaluation" / "consistency.md"
    existing = ""
    if eval_path.exists():
        existing = eval_path.read_text(encoding="utf-8")
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
            payloads = [json.loads(f.read_text(encoding="utf-8")) for f in result_files]
            data[experiment_id][role] = payloads

    return data


def _avg(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def _format_value(value: Optional[float], digits: int = 2) -> str:
    if value is None:
        return "n/a"
    return f"{value:.{digits}f}"


def _format_ratio(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    return f"{value:.1%}"


def _write_evaluation_reports(results_path: str) -> None:
    data = _collect_results(results_path)
    eval_dir = Path(results_path) / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    def build_scores(experiment_id: str) -> str:
        roles = data.get(experiment_id, {})
        lines = [
            f"# Scores {experiment_id}",
            "",
            "| role | total | correct | accuracy | avg_confidence | avg_attempts | avg_textual_score | avg_math_delta |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        breakdown_lines = [
            "",
            "## Task breakdown",
            "",
            "| role | task_id | total | correct | accuracy |",
            "| --- | --- | --- | --- | --- |",
        ]

        reasoning_lines = [
            "",
            "## Reasoning differences",
            "",
            "| role | task_id | repetitions | reasoning_consistent | reasoning_samples |",
            "| --- | --- | --- | --- | --- |",
        ]

        reasoning_full_lines = [
            "",
            "## Reasoning samples (full)",
            "",
        ]

        for role, payloads in sorted(roles.items()):
            total = len(payloads)
            correct = sum(1 for p in payloads if p.get("verdict") == "correct")
            accuracy = (correct / total) if total else None
            avg_attempts = _avg([float(p.get("attempts", 0)) for p in payloads])
            confidences = []
            for p in payloads:
                final_answer = p.get("final_answer", {})
                confidence = final_answer.get("confidence") if isinstance(final_answer, dict) else None
                if isinstance(confidence, (int, float)):
                    confidences.append(float(confidence))

            textual_scores = [
                float(p.get("judge_score", {}).get("total_score", 0))
                for p in payloads
                if p.get("task_type") == "textual"
            ]
            math_deltas = [
                float(p.get("judge_score", {}).get("delta", 0))
                for p in payloads
                if p.get("task_type") == "math"
            ]

            lines.append(
                "| {role} | {total} | {correct} | {accuracy} | {avg_confidence} | {avg_attempts} | {avg_textual} | {avg_delta} |".format(
                    role=role,
                    total=total,
                    correct=correct,
                    accuracy=_format_ratio(accuracy),
                    avg_confidence=_format_value(_avg(confidences), digits=3),
                    avg_attempts=_format_value(avg_attempts, digits=2),
                    avg_textual=_format_value(_avg(textual_scores), digits=2),
                    avg_delta=_format_value(_avg(math_deltas), digits=3),
                )
            )

            per_task: Dict[str, List[Dict[str, Any]]] = {}
            for payload in payloads:
                per_task.setdefault(payload.get("task_id", "unknown"), []).append(payload)
            for task_id, task_payloads in sorted(per_task.items()):
                task_total = len(task_payloads)
                task_correct = sum(1 for p in task_payloads if p.get("verdict") == "correct")
                task_accuracy = (task_correct / task_total) if task_total else None
                breakdown_lines.append(
                    "| {role} | {task_id} | {total} | {correct} | {accuracy} |".format(
                        role=role,
                        task_id=task_id,
                        total=task_total,
                        correct=task_correct,
                        accuracy=_format_ratio(task_accuracy),
                    )
                )
                reasoning_values = []
                for p in task_payloads:
                    final_answer = p.get("final_answer", {})
                    reasoning = final_answer.get("reasoning") if isinstance(final_answer, dict) else None
                    if isinstance(reasoning, str):
                        reasoning_values.append(reasoning.strip())
                reasoning_unique = {r for r in reasoning_values if r}
                reasoning_consistent = "yes" if len(reasoning_unique) <= 1 else "no"
                sample_list = sorted(reasoning_unique)[:2]
                if not sample_list:
                    sample_text = "n/a"
                elif len(sample_list) == 1:
                    sample_text = sample_list[0]
                else:
                    sample_text = " / ".join(sample_list)
                reasoning_lines.append(
                    "| {role} | {task_id} | {total} | {consistent} | {samples} |".format(
                        role=role,
                        task_id=task_id,
                        total=task_total,
                        consistent=reasoning_consistent,
                        samples=sample_text.replace("\n", " "),
                    )
                )

                reasoning_full_lines.append(f"### {role} - {task_id}")
                for idx, payload in enumerate(task_payloads, start=1):
                    final_answer = payload.get("final_answer", {})
                    reasoning = final_answer.get("reasoning") if isinstance(final_answer, dict) else None
                    rep_value = payload.get("repetition", idx)
                    if isinstance(reasoning, str) and reasoning.strip():
                        reasoning_full_lines.append(
                            f"rep {rep_value}: {reasoning.strip().replace('\n', ' ')}"
                        )
                    else:
                        reasoning_full_lines.append(f"rep {rep_value}: n/a")
                reasoning_full_lines.append("")

        return "\n".join(lines + breakdown_lines + reasoning_lines + reasoning_full_lines) + "\n"

    for experiment_id in ["1A", "1B"]:
        report = build_scores(experiment_id)
        report_path = eval_dir / f"scores_{experiment_id}.md"
        report_path.write_text(report, encoding="utf-8")

    comparison_lines = [
        "# Comparison 1A vs 1B",
        "",
        "| role | accuracy_1A | accuracy_1B | delta |",
        "| --- | --- | --- | --- |",
    ]

    for role in ["expert", "beginner"]:
        acc_1a_payloads = data.get("1A", {}).get(role, [])
        acc_1b_payloads = data.get("1B", {}).get(role, [])
        acc_1a = None
        acc_1b = None
        if acc_1a_payloads:
            acc_1a = sum(1 for p in acc_1a_payloads if p.get("verdict") == "correct") / len(
                acc_1a_payloads
            )
        if acc_1b_payloads:
            acc_1b = sum(1 for p in acc_1b_payloads if p.get("verdict") == "correct") / len(
                acc_1b_payloads
            )
        delta = (acc_1b - acc_1a) if acc_1a is not None and acc_1b is not None else None
        comparison_lines.append(
            "| {role} | {acc_1a} | {acc_1b} | {delta} |".format(
                role=role,
                acc_1a=_format_ratio(acc_1a),
                acc_1b=_format_ratio(acc_1b),
                delta=_format_ratio(delta) if delta is not None else "n/a",
            )
        )

    comparison_path = eval_dir / "comparison.md"
    comparison_path.write_text("\n".join(comparison_lines) + "\n", encoding="utf-8")
