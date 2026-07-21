"""Task parsing and result lookup helpers."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


def _slugify(value: str) -> str:
    """Sanitize a string for use in filenames: replace non-alphanumeric chars with _."""
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_")


def _model_slug(model: str, is_hosted: bool) -> str:
    """Build the filename slug for a model, prefixing 'hosted_' for cloud runs."""
    slug = _slugify(model)
    return f"hosted_{slug}" if is_hosted else slug


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
    import config
    from utils.cvss_utils import inject_cvss_instructions, is_cvss_task
    from utils.sast_hint import build_sast_hint_block

    task_path = Path(state["task_path"])
    sol_path = Path(state["sol_path"])

    # task_content below is read verbatim from docs/tasks/<task>.md and IS the
    # prompt body sent to the agent (scenario + code + per-task output-format
    # instructions) — see agents/prompts.py for where this fits in the full
    # assembly order and for every other prompt-contributing piece.
    task_content = _read_text(task_path)
    sol_content = _read_text(sol_path)
    metadata = _parse_task_metadata(task_content)
    json_blocks = _extract_json_blocks(sol_content)

    ground_truth = json_blocks[0] if json_blocks else {}
    rubric = json_blocks[1] if len(json_blocks) > 1 else {}

    if config.SAST_HINT_ENABLED:
        task_content += build_sast_hint_block(metadata["task_id"], config.SAST_HINT_DATASET_PATH)

    if config.CVSS_ESTIMATE_ENABLED and is_cvss_task(metadata["task_id"], metadata["task_type"]):
        task_content = inject_cvss_instructions(task_content)

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


def _result_exists(results_path: str, experiment_id: str, role: str, task_id: str, repetition: int, model: str, is_hosted: bool = False) -> bool:
    result_path = (
        Path(results_path)
        / task_id
        / experiment_id
        / role
        / f"{_model_slug(model, is_hosted)}.json"
    )
    if not result_path.exists():
        return False
    try:
        data = json.loads(result_path.read_text(encoding="utf-8"))
        return any(r.get("repetition") == repetition for r in data.get("repetitions", []))
    except Exception:
        return False


def _answers_equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
