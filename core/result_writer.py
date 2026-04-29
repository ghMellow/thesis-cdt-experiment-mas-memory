import json
from pathlib import Path
from typing import Any, Dict


def write_result(
    base_path: str,
    experiment_id: str,
    role: str,
    task_id: str,
    repetition: int,
    result_payload: Dict[str, Any],
    ground_truth: Dict[str, Any],
) -> None:
    out_dir = Path(base_path) / experiment_id / role
    out_dir.mkdir(parents=True, exist_ok=True)

    prefix = f"{task_id}_rep{repetition}"
    result_path = out_dir / f"{prefix}.json"
    solution_path = out_dir / f"{prefix}_solution.json"

    result_path.write_text(json.dumps(result_payload, indent=2, ensure_ascii=True))
    solution_payload = {"task_id": task_id, "ground_truth": ground_truth}
    solution_path.write_text(json.dumps(solution_payload, indent=2, ensure_ascii=True))
