"""Experiment orchestration helpers."""

import json
import logging
import signal
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict

import httpx
from langgraph.graph import END, StateGraph

logger = logging.getLogger(__name__)

from agents._llm_utils import _expected_score_fields
from agents.agent_runner import run_agent
from agents.judge_agent import run_judge_textual
from agents.prompts import SYSTEM_PROMPTS
import config
from agents._llm_utils import resolve_model_config
from utils.task_utils import _model_slug
from config import (
    MAX_RETRIES,
    MODELS,
    OLLAMA_BASE_URL,
    TEMPERATURE,
    TEXTUAL_PASS_RATIO,
)
from utils.task_utils import _load_task


def _fetch_model_context_window(model: str, base_url: str) -> Optional[int]:
    """Query Ollama /api/show and return the model's context length, or None on failure."""
    try:
        resp = httpx.post(f"{base_url}/api/show", json={"model": model}, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        for key, val in data.get("model_info", {}).items():
            if "context_length" in key:
                return int(val)
        for line in data.get("parameters", "").splitlines():
            parts = line.strip().split()
            if parts and parts[0].lower() == "num_ctx":
                return int(parts[-1])
    except Exception:
        pass
    return None


def _build_judge_prompt(rubric: Dict[str, Any]) -> str:
    """Generate a judge system prompt tailored to the task's rubric categories."""
    rubric_items = rubric.get("rubrica", {})
    total_max = rubric.get("total_max", 0)

    criteria_lines = []
    for field, spec in rubric_items.items():
        max_val = spec.get("max", 0)
        criteri = spec.get("criteri", {})
        criteria_text = "; ".join(
            f"{k}={v}" for k, v in sorted(criteri.items(), key=lambda x: x[0], reverse=True)
        )
        criteria_lines.append(f"- {field} (0–{max_val}): {criteria_text}")


    criteria_block = "\n".join(criteria_lines)
    expected_fields = _expected_score_fields(rubric)
    output_lines = ["## Scores"]
    output_lines.extend([f"{field}: 0" for field in expected_fields])
    output_lines += ["", "## Feedback", "..."]
    output_template = "\n".join(output_lines)

    return (
        "You are an expert evaluator of technical responses about 5G networks.\n"
        "Evaluate the agent's response using the rubric criteria below.\n"
        f"Total maximum score: {total_max}\n\n"
        f"Scoring criteria:\n{criteria_block}\n\n"
        "Reply ONLY with Markdown using this exact template:\n"
        f"{output_template}\n"
        "No text outside the Markdown."
    )


def _to_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.strip())
    raise ValueError(f"Unsupported numeric value: {value}")


def _check_math_answer(
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
        return "correct" if delta == 0 else "wrong", float(delta), "exact int check"

    if gt_type == "real":
        if isinstance(gt_answer, dict):
            received_obj = agent_answer.get("answer", {})
            deltas = {
                key: abs(_to_float(received_obj.get(key)) - float(expected_value))
                for key, expected_value in gt_answer.items()
            }
            delta = max(deltas.values()) if deltas else 0.0
            verdict = "correct" if all(d <= tolerance for d in deltas.values()) else "wrong"
            return verdict, delta, f"real check with tolerance {tolerance}"

        expected = float(gt_answer)
        received = _to_float(agent_answer.get("answer"))
        delta = abs(received - expected)
        return "correct" if delta <= tolerance else "wrong", delta, f"real check with tolerance {tolerance}"

    raise ValueError(f"Unsupported ground truth type: {gt_type}")


class ExperimentState(TypedDict, total=False):
    task_id: str
    task_type: str
    task_content: str
    ground_truth: Dict[str, Any]
    rubric: Dict[str, Any]
    agent_role: str
    model: str
    is_hosted: bool
    attempts: int
    history: List[Dict[str, Any]]
    verdict: str
    judge_score: Dict[str, Any]
    final_answer: Dict[str, Any]
    agent_tokens_in: int
    agent_tokens_out: int
    judge_tokens_in: int
    judge_tokens_out: int
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


def _format_previous_answer(answer: Any) -> str:
    if isinstance(answer, dict):
        lines: List[str] = []
        for key, value in answer.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                lines.extend([f"- {entry}" for entry in value])
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines) if lines else ""
    if isinstance(answer, list):
        return "\n".join([f"- {entry}" for entry in answer])
    return str(answer)


def _build_retry_task_content(task_content: str, history: list) -> str:
    last = history[-1]
    prev_reasoning = last.get("reasoning", "")
    prev_answer = _format_previous_answer(last.get("answer", ""))
    prev_confidence = last.get("confidence", "")
    return (
        f"{task_content}\n\n"
        "---\n"
        "Note: you already attempted this task. Review your previous attempt below, "
        "then try again from scratch.\n\n"
        "### Previous Answer\n"
        f"{prev_answer}\n\n"
        "### Previous Reasoning\n"
        f"{prev_reasoning}\n\n"
        "### Previous Confidence\n"
        f"{prev_confidence}\n\n"
        "Please reason again from scratch and follow the response format in the task."
    )


def _run_agent(state: ExperimentState) -> ExperimentState:
    role = state["agent_role"]
    system_prompt = SYSTEM_PROMPTS[role]
    history = state.get("history", [])
    task_content = (
        _build_retry_task_content(state["task_content"], history)
        if history
        else state["task_content"]
    )
    agent_response, in_tok, out_tok = run_agent(
        task_content=task_content,
        system_prompt=system_prompt,
        model=state["model"],
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        is_hosted=state.get("is_hosted", False),
    )

    attempts = state.get("attempts", 0) + 1
    history = state.get("history", [])
    history.append(agent_response)

    state.update(
        {
            "attempts": attempts,
            "history": history,
            "final_answer": agent_response,
            "agent_tokens_in": state.get("agent_tokens_in", 0) + (in_tok or 0),
            "agent_tokens_out": state.get("agent_tokens_out", 0) + (out_tok or 0),
        }
    )
    return state


def _check_answer(state: ExperimentState) -> ExperimentState:
    if state["task_type"] == "math":
        verdict, delta, note = _check_math_answer(
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

    rubric = state.get("rubric", {})
    judge_model, judge_is_hosted = resolve_model_config("judge")
    judge_score, j_in_tok, j_out_tok = run_judge_textual(
        task_content=state["task_content"],
        rubric=rubric,
        agent_response=state["final_answer"],
        system_prompt=_build_judge_prompt(rubric),
        model=judge_model,
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        is_hosted=judge_is_hosted,
    )
    state.update(
        {
            "judge_tokens_in": state.get("judge_tokens_in", 0) + (j_in_tok or 0),
            "judge_tokens_out": state.get("judge_tokens_out", 0) + (j_out_tok or 0),
        }
    )

    total_score = judge_score.get("total_score")
    if total_score is None:
        total_score = sum(
            v for k, v in judge_score.items()
            if k.endswith("_score") and k != "total_score" and isinstance(v, (int, float))
        )
        judge_score["total_score"] = total_score

    total_max = rubric.get("total_max", 0)
    total_score = float(min(max(float(total_score), 0.0), float(total_max)) if total_max else float(total_score))
    judge_score["total_score"] = total_score
    normalized = round(total_score / total_max, 3) if total_max else 0.0
    judge_score["normalized_score"] = normalized

    verdict = "correct" if total_max and normalized >= TEXTUAL_PASS_RATIO else "wrong"
    
    # Print rubric breakdown and verdict to stdout
    logger.info("=== Judge Evaluation ===")
    for field, score in judge_score.items():
        if field.endswith("_score") and field != "total_score":
            logger.info("  %s: %s", field, score)
    logger.info("  total_score: %.1f / %d (normalized: %.1f)", total_score, total_max, normalized)
    logger.info("  threshold: %.1f | verdict: %s", TEXTUAL_PASS_RATIO, verdict)
    
    state.update({"verdict": verdict, "judge_score": judge_score})
    return state


def _save_result(state: ExperimentState) -> ExperimentState:
    finished_at = datetime.now(timezone.utc).isoformat()
    start_perf = state.get("start_perf")
    elapsed_seconds = time.perf_counter() - start_perf if start_perf is not None else None
    payload = {
        # --- run config ---
        "task_id": state["task_id"],
        "task_type": state["task_type"],
        "experiment_id": state["experiment_id"],
        "agent_role": state["agent_role"],
        "model": state["model"],
        "is_hosted": state.get("is_hosted", False),
        "repetition": state["repetition"],
        "task_path": state["task_path"],
        "sol_path": state["sol_path"],
        # --- timing ---
        "started_at": state.get("started_at"),
        "finished_at": finished_at,
        "elapsed_seconds": elapsed_seconds,
        # --- agent ---
        "attempts": state["attempts"],
        "history": state["history"],
        "final_answer": state["final_answer"],
        # --- judge ---
        "verdict": state["verdict"],
        "judge_score": state.get("judge_score", {}),
        # --- resources ---
        "tokens": {
            "agent_in": state.get("agent_tokens_in") or None,
            "agent_out": state.get("agent_tokens_out") or None,
            "judge_in": state.get("judge_tokens_in") or None,
            "judge_out": state.get("judge_tokens_out") or None,
        },
    }
    out_dir = (
        Path(config.RESULTS_PATH)
        / state["task_id"]
        / state["experiment_id"]
        / state["agent_role"]
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"rep{state['repetition']}_{_model_slug(state['model'], state.get('is_hosted', False))}"
    (out_dir / f"{prefix}.json").write_text(json.dumps(payload, indent=2, ensure_ascii=True))
    solution_payload = {"task_id": state["task_id"], "ground_truth": state["ground_truth"]}
    (out_dir / f"{prefix}_solution.json").write_text(json.dumps(solution_payload, indent=2, ensure_ascii=True))
    return state


def _route_after_check(state: ExperimentState) -> str:
    if state["verdict"] != "correct" and state["attempts"] < MAX_RETRIES:
        logger.info(
            "verdict=wrong → retry attempt %d/%d",
            state["attempts"] + 1,
            MAX_RETRIES,
        )
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
