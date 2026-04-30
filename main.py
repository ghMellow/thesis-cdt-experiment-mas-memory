"""Entry point and orchestration; task parsing and evaluation helpers live in utils."""

import argparse
import logging
import signal
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph

from agents.agent_runner import run_agent
from agents.judge_agent import run_judge_textual
from agents.prompts import SYSTEM_PROMPTS
import config
from config import (
    MAX_RETRIES,
    MODELS,
    OLLAMA_BASE_URL,
    REPETITIONS,
    RESULTS_PATH,
    TASK_TIMEOUT_SECONDS,
    TASKS_PATH,
    TEMPERATURE,
    TEXTUAL_PASS_RATIO,
)
from core.checker import check_math_answer
from core.loop_controller import should_retry
from core.result_writer import write_result
from utils.evaluation_utils import _record_consistency_finding, _write_evaluation_reports
from utils.task_utils import _answers_equal, _list_tasks, _load_task, _result_exists


logger = logging.getLogger(__name__)


@contextmanager
def _time_limit(seconds: int):
    if seconds <= 0:
        yield
        return

    def _handle_timeout(signum: int, frame) -> None:
        raise TimeoutError("Task timed out")

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


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
    started_at: str
    finished_at: str
    elapsed_seconds: float
    start_perf: float



def _run_agent(state: ExperimentState) -> ExperimentState:
    role = state["agent_role"]
    system_prompt = SYSTEM_PROMPTS[role]
    agent_response = run_agent(
        task_content=state["task_content"],
        system_prompt=system_prompt,
        model=state["model"],
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        role=state["agent_role"],
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
    finished_at = datetime.now(timezone.utc).isoformat()
    elapsed_seconds = None
    start_perf = state.get("start_perf")
    if start_perf is not None:
        elapsed_seconds = time.perf_counter() - start_perf
    payload = {
        "task_id": state["task_id"],
        "task_type": state["task_type"],
        "task_path": state["task_path"],
        "sol_path": state["sol_path"],
        "agent_role": state["agent_role"],
        "model": state["model"],
        "repetition": state["repetition"],
        "started_at": state.get("started_at"),
        "finished_at": finished_at,
        "elapsed_seconds": elapsed_seconds,
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



def main() -> None:
    parser = argparse.ArgumentParser(description="Run multi-agent experiments")
    parser.add_argument(
        "--experiment",
        choices=["1A", "1B", "all"],
        default="all",
        help="Select experiment group",
    )
    parser.add_argument(
        "--role",
        choices=["expert", "beginner", "all"],
        default="all",
        help="Select agent role",
    )
    parser.add_argument(
        "--task",
        action="append",
        dest="tasks",
        help="Filter by task id (can be repeated)",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=REPETITIONS,
        help="Override repetitions per task",
    )
    parser.add_argument(
        "--task-timeout",
        type=int,
        default=TASK_TIMEOUT_SECONDS,
        help="Max seconds per task repetition (0 = no timeout)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    graph = _build_graph()
    tasks = _list_tasks(TASKS_PATH)
    if args.tasks:
        available = {task.stem for task in tasks}
        requested = set(args.tasks)
        missing = sorted(requested - available)
        if missing:
            logger.error("Unknown task ids: %s", ", ".join(missing))
            raise SystemExit(1)
        tasks = [task for task in tasks if task.stem in requested]

    experiments = [
        {"id": "1A", "role": "expert", "model": MODELS["expert_1A"]},
        {"id": "1A", "role": "beginner", "model": MODELS["beginner_1A"]},
        {"id": "1B", "role": "expert", "model": MODELS["expert_1B"]},
        {"id": "1B", "role": "beginner", "model": MODELS["beginner_1B"]},
    ]
    if args.experiment != "all":
        experiments = [exp for exp in experiments if exp["id"] == args.experiment]
    if args.role != "all":
        experiments = [exp for exp in experiments if exp["role"] == args.role]
    if not experiments:
        raise ValueError("No experiments matched the provided filters")

    remaining_repetitions = 0
    for experiment in experiments:
        for task_path in tasks:
            for repetition in range(1, args.repetitions + 1):
                if _result_exists(
                    RESULTS_PATH,
                    experiment["id"],
                    experiment["role"],
                    task_path.stem,
                    repetition,
                ):
                    continue
                remaining_repetitions += 1

    desired_ollama_timeout = int(args.task_timeout * 1.1)
    if desired_ollama_timeout > config.OLLAMA_TIMEOUT_SECONDS:
        config.OLLAMA_TIMEOUT_SECONDS = desired_ollama_timeout

    worst_case_seconds = remaining_repetitions * args.task_timeout
    worst_case_hours = worst_case_seconds // 3600
    worst_case_minutes = (worst_case_seconds % 3600) // 60
    worst_case_secs = worst_case_seconds % 60
    worst_case_hms = f"{worst_case_hours}h {worst_case_minutes}m {worst_case_secs}s"
    logger.info(
        "worst-case max time: %s | Ollama timeout: %ss | Remaining repetitions: %s",
        worst_case_hms,
        config.OLLAMA_TIMEOUT_SECONDS,
        remaining_repetitions,
    )

    consistency_lines: List[str] = []

    for experiment in experiments:
        logger.info("")
        logger.info(
            "==== Experiment %s | role=%s | model=%s ====",
            experiment["id"],
            experiment["role"],
            experiment["model"],
        )
        for task_path in tasks:
            logger.info("")
            logger.info("---- Task %s ----", task_path.stem)
            sol_path = task_path.with_name(task_path.stem + "_sol.md")
            previous_answer: Optional[Dict[str, Any]] = None

            for repetition in range(1, args.repetitions + 1):
                if _result_exists(
                    RESULTS_PATH,
                    experiment["id"],
                    experiment["role"],
                    task_path.stem,
                    repetition,
                ):
                    logger.info("Skip %s rep %s (already exists)", task_path.stem, repetition)
                    continue
                logger.info("Repetition %s/%s", repetition, args.repetitions)
                started_at = datetime.now(timezone.utc).isoformat()
                start_perf = time.perf_counter()
                initial_state: ExperimentState = {
                    "task_path": str(task_path),
                    "sol_path": str(sol_path),
                    "agent_role": experiment["role"],
                    "model": experiment["model"],
                    "attempts": 0,
                    "history": [],
                    "experiment_id": experiment["id"],
                    "repetition": repetition,
                    "started_at": started_at,
                    "start_perf": start_perf,
                }
                try:
                    with _time_limit(args.task_timeout):
                        result_state = graph.invoke(initial_state)
                except TimeoutError:
                    logger.warning(
                        "Timeout after %ss | %s rep %s",
                        args.task_timeout,
                        task_path.stem,
                        repetition,
                    )
                    logger.error("Exiting after timeout to allow manual restart of Ollama")
                    raise SystemExit(1)
                final_answer = result_state.get("final_answer", {})
                logger.info(
                    "Done %s rep %s | verdict=%s | attempts=%s",
                    result_state.get("task_id", task_path.stem),
                    repetition,
                    result_state.get("verdict"),
                    result_state.get("attempts"),
                )

                if previous_answer is not None and not _answers_equal(previous_answer, final_answer):
                    consistency_lines.append(
                        f"- {experiment['id']} {experiment['role']} {result_state['task_id']}: "
                        f"rep {repetition} differs from rep {repetition - 1}"
                    )
                previous_answer = final_answer

    _record_consistency_finding(consistency_lines)
    logger.info("Writing evaluation reports")
    _write_evaluation_reports(RESULTS_PATH)
    logger.info("Execution complete")


if __name__ == "__main__":
    main()
