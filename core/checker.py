from typing import Any, Dict, Tuple


def _to_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.strip())
    raise ValueError(f"Unsupported numeric value: {value}")


def _max_delta(deltas: Dict[str, float]) -> float:
    return max(deltas.values()) if deltas else 0.0


def check_math_answer(
    agent_answer: Dict[str, Any],
    ground_truth: Dict[str, Any],
) -> Tuple[str, float, str]:
    gt_answer = ground_truth.get("answer")
    gt_type = ground_truth.get("type")
    tolerance = float(ground_truth.get("tolerance", 0))

    if gt_type == "exact_int":
        expected = int(gt_answer)
        received = int(_to_float(agent_answer.get("answer")))
        delta = abs(received - expected)
        verdict = "correct" if delta == 0 else "wrong"
        note = "exact int check"
        return verdict, float(delta), note

    if gt_type == "real":
        if isinstance(gt_answer, dict):
            received_obj = agent_answer.get("answer", {})
            deltas = {}
            for key, expected_value in gt_answer.items():
                received_value = received_obj.get(key)
                deltas[key] = abs(_to_float(received_value) - float(expected_value))
            delta = _max_delta(deltas)
            verdict = "correct" if all(d <= tolerance for d in deltas.values()) else "wrong"
            note = f"real check with tolerance {tolerance}"
            return verdict, delta, note

        expected = float(gt_answer)
        received = _to_float(agent_answer.get("answer"))
        delta = abs(received - expected)
        verdict = "correct" if delta <= tolerance else "wrong"
        note = f"real check with tolerance {tolerance}"
        return verdict, delta, note

    raise ValueError(f"Unsupported ground truth type: {gt_type}")
