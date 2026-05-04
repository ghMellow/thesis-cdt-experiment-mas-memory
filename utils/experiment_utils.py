"""Experiment orchestration helpers."""

import signal
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from agents.agent_runner import run_agent
from agents.judge_agent import run_judge_textual
from agents.prompts import SYSTEM_PROMPTS
import config
from config import (
    MAX_RETRIES,
    MODELS,
    OLLAMA_BASE_URL,
    TEMPERATURE,
    TEXTUAL_PASS_RATIO,
)
from core.checker import check_math_answer
from core.loop_controller import should_retry
from core.result_writer import write_result
from utils.task_utils import _load_task


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
        base_path=config.RESULTS_PATH,
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
