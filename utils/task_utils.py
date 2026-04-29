"""Task parsing and result lookup helpers."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_task_metadata(task_content: str) -> Dict[str, str]:
    task_id_match = re.search(r"\*\*ID:\*\*\s*(.+)", task_content)
    task_type_match = re.search(r"\*\*Tipo:\*\*\s*(.+)", task_content)
    if not task_id_match or not task_type_match:
        raise ValueError("Task metadata not found")
    return {
        "task_id": task_id_match.group(1).strip(),
        "task_type": task_type_match.group(1).strip(),
    }


def _extract_json_blocks(text: str) -> List[Dict[str, Any]]:
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    return [json.loads(block) for block in blocks]


def _load_task(state: "ExperimentState") -> "ExperimentState":
    task_path = Path(state["task_path"])
    sol_path = Path(state["sol_path"])

    task_content = _read_text(task_path)
    sol_content = _read_text(sol_path)
    metadata = _parse_task_metadata(task_content)
    json_blocks = _extract_json_blocks(sol_content)

    ground_truth = json_blocks[0] if json_blocks else {}
    rubric = json_blocks[1] if len(json_blocks) > 1 else {}

    state.update(
        {
            "task_id": metadata["task_id"],
            "task_type": metadata["task_type"],
            "task_content": task_content,
            "ground_truth": ground_truth,
            "rubric": rubric,
        }
    )
    return state


def _list_tasks(tasks_path: str) -> List[Path]:
    base = Path(tasks_path)
    return sorted(p for p in base.glob("*.md") if not p.name.endswith("_sol.md"))


def _result_exists(results_path: str, experiment_id: str, role: str, task_id: str, repetition: int) -> bool:
    result_path = (
        Path(results_path)
        / experiment_id
        / role
        / f"{task_id}_rep{repetition}.json"
    )
    return result_path.exists()


def _answers_equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
