import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph

from agents.agent_runner import run_agent
from agents.judge_agent import run_judge_textual
from agents.prompts import SYSTEM_PROMPTS
from config import (
    MAX_RETRIES,
    MODELS,
    OLLAMA_BASE_URL,
    REPETITIONS,
    RESULTS_PATH,
    TASKS_PATH,
    TEMPERATURE,
    TEXTUAL_PASS_RATIO,
)
from core.checker import check_math_answer
from core.loop_controller import should_retry
from core.result_writer import write_result


class ExperimentState(TypedDict, total=False):
    task_id: str
    task_type: str
    task_content: str
    ground_truth: Dict[str, Any]
    rubric: Dict[str, Any]
    agent_role: str
    model: str
    attempts: int
    history: List[Dict[str, Any]]
    verdict: str
    judge_score: Dict[str, Any]
    final_answer: Dict[str, Any]
    task_path: str
    sol_path: str
    experiment_id: str
    repetition: int


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


def _load_task(state: ExperimentState) -> ExperimentState:
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


def _run_agent(state: ExperimentState) -> ExperimentState:
    role = state["agent_role"]
    system_prompt = SYSTEM_PROMPTS[role]
    agent_response = run_agent(
        task_content=state["task_content"],
        system_prompt=system_prompt,
        model=state["model"],
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
    )

    attempts = state.get("attempts", 0) + 1
    history = state.get("history", [])
    history.append(agent_response)

    state.update(
        {
            "attempts": attempts,
            "history": history,
            "final_answer": agent_response,
        }
    )
    return state


def _check_answer(state: ExperimentState) -> ExperimentState:
    if state["task_type"] == "math":
        verdict, delta, note = check_math_answer(
            agent_answer=state["final_answer"],
            ground_truth=state["ground_truth"],
        )
        state.update(
            {
                "verdict": verdict,
                "judge_score": {"verdict": verdict, "delta": delta, "note": note},
            }
        )
        return state

    judge_score = run_judge_textual(
        task_content=state["task_content"],
        rubric=state.get("rubric", {}),
        agent_response=state["final_answer"],
        system_prompt=SYSTEM_PROMPTS["judge_textual"],
        model=MODELS["judge"],
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
    )

    total_score = judge_score.get("total_score")
    if total_score is None:
        total_score = sum(
            v for k, v in judge_score.items() if k.endswith("_score") and k != "total_score"
        )
        judge_score["total_score"] = total_score

    total_max = 0
    rubric = state.get("rubric", {})
    if rubric:
        total_max = rubric.get("total_max", 0)
    verdict = "correct" if total_max and total_score >= total_max * TEXTUAL_PASS_RATIO else "wrong"

    state.update({"verdict": verdict, "judge_score": judge_score})
    return state


def _save_result(state: ExperimentState) -> ExperimentState:
    payload = {
        "task_id": state["task_id"],
        "task_type": state["task_type"],
        "task_path": state["task_path"],
        "sol_path": state["sol_path"],
        "agent_role": state["agent_role"],
        "model": state["model"],
        "attempts": state["attempts"],
        "history": state["history"],
        "verdict": state["verdict"],
        "judge_score": state.get("judge_score", {}),
        "final_answer": state["final_answer"],
    }
    write_result(
        base_path=RESULTS_PATH,
        experiment_id=state["experiment_id"],
        role=state["agent_role"],
        task_id=state["task_id"],
        repetition=state["repetition"],
        result_payload=payload,
        ground_truth=state["ground_truth"],
    )
    return state


def _route_after_check(state: ExperimentState) -> str:
    if should_retry(state["attempts"], MAX_RETRIES, state["verdict"]):
        return "retry"
    return "save"


def _build_graph() -> Any:
    graph = StateGraph(ExperimentState)
    graph.add_node("load_task", _load_task)
    graph.add_node("run_agent", _run_agent)
    graph.add_node("check_answer", _check_answer)
    graph.add_node("save_result", _save_result)

    graph.set_entry_point("load_task")
    graph.add_edge("load_task", "run_agent")
    graph.add_edge("run_agent", "check_answer")
    graph.add_conditional_edges(
        "check_answer", _route_after_check, {"retry": "run_agent", "save": "save_result"}
    )
    graph.add_edge("save_result", END)

    return graph.compile()


def _list_tasks(tasks_path: str) -> List[Path]:
    base = Path(tasks_path)
    return sorted(p for p in base.glob("*.md") if not p.name.endswith("_sol.md"))


def _answers_equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def _record_consistency_finding(lines: List[str]) -> None:
    if not lines:
        return
    eval_path = Path(RESULTS_PATH) / "evaluation" / "consistency.md"
    existing = ""
    if eval_path.exists():
        existing = eval_path.read_text(encoding="utf-8")
    content = existing + "\n" + "\n".join(lines) + "\n"
    eval_path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    graph = _build_graph()
    tasks = _list_tasks(TASKS_PATH)

    experiments = [
        {"id": "1A", "role": "expert", "model": MODELS["expert_1A"]},
        {"id": "1A", "role": "beginner", "model": MODELS["beginner_1A"]},
        {"id": "1B", "role": "expert", "model": MODELS["expert_1B"]},
        {"id": "1B", "role": "beginner", "model": MODELS["beginner_1B"]},
    ]

    consistency_lines: List[str] = []

    for experiment in experiments:
        for task_path in tasks:
            sol_path = task_path.with_name(task_path.stem + "_sol.md")
            previous_answer: Optional[Dict[str, Any]] = None

            for repetition in range(1, REPETITIONS + 1):
                initial_state: ExperimentState = {
                    "task_path": str(task_path),
                    "sol_path": str(sol_path),
                    "agent_role": experiment["role"],
                    "model": experiment["model"],
                    "attempts": 0,
                    "history": [],
                    "experiment_id": experiment["id"],
                    "repetition": repetition,
                }

                result_state = graph.invoke(initial_state)
                final_answer = result_state.get("final_answer", {})

                if previous_answer is not None and not _answers_equal(previous_answer, final_answer):
                    consistency_lines.append(
                        f"- {experiment['id']} {experiment['role']} {result_state['task_id']}: "
                        f"rep {repetition} differs from rep {repetition - 1}"
                    )
                previous_answer = final_answer

    _record_consistency_finding(consistency_lines)


if __name__ == "__main__":
    main()
