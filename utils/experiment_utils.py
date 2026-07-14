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

from agents.agent_runner import run_agent
from agents.judge_agent import run_judge_textual
from agents.prompts import SYSTEM_PROMPTS
import config
from agents._llm_utils import _expected_score_fields, resolve_model_config
from utils.task_utils import _model_slug
from config import (
    MAX_RETRIES,
    MODELS,
    OLLAMA_BASE_URL,
    TEXTUAL_PASS_RATIO,
)
from utils.task_utils import _load_task
from utils.cvss_eval import evaluate_cvss_estimate
from utils.cvss_utils import is_cvss_task
from utils.sgv import run_sgv


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


def build_judge_prompt(rubric: Dict[str, Any]) -> str:
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
    run_id: str
    started_at: str
    finished_at: str
    elapsed_seconds: float
    start_perf: float
    sgv_passed: bool
    sgv_feedback: Optional[str]


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


def build_retry_task_content(
    task_content: str, history: list, sgv_feedback: Optional[str] = None
) -> str:
    last = history[-1]
    prev_reasoning = last.get("reasoning", "")
    prev_answer = _format_previous_answer(last.get("answer", ""))
    prev_confidence = last.get("confidence", "")
    content = (
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
    )
    if sgv_feedback:
        # SGV (docs/sgv_protocol/): purely formal feedback, never states which
        # function is actually vulnerable — only what is malformed/ungrounded.
        content += (
            "### Formal Issues Found In Your CVSS Estimate (fix these — this is "
            "NOT about whether the code is vulnerable, only about the report's form)\n"
            f"{sgv_feedback}\n\n"
        )
    content += "Please reason again from scratch and follow the response format in the task."
    return content


def _run_agent(state: ExperimentState) -> ExperimentState:
    role = state["agent_role"]
    system_prompt = SYSTEM_PROMPTS[role]
    history = state.get("history", [])
    task_content = (
        build_retry_task_content(state["task_content"], history, state.get("sgv_feedback"))
        if history
        else state["task_content"]
    )
    t0 = time.perf_counter()
    agent_response, in_tok, out_tok = run_agent(
        task_content=task_content,
        system_prompt=system_prompt,
        model=state["model"],
        temperature=config.TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        is_hosted=state.get("is_hosted", False),
    )
    agent_response["elapsed_seconds"] = round(time.perf_counter() - t0, 2)
    agent_response["tokens_in"] = in_tok
    agent_response["tokens_out"] = out_tok
    agent_response["prompt_system"] = system_prompt
    agent_response["prompt_user"] = task_content

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


def _check_sgv(state: ExperimentState) -> ExperimentState:
    """SGV gate (docs/sgv_protocol/): deterministic, no ground truth, applied
    once per finding before the rubric/CVSS branches split. Only runs on
    security-review tasks that carry a CVSS Estimate; a no-op otherwise."""
    if not (getattr(config, "SGV_ENABLED", False) and is_cvss_task(state["task_id"], state["task_type"])):
        state.update({"sgv_passed": True, "sgv_feedback": None})
        return state

    cvss_estimate = state["final_answer"].get("cvss_estimate")
    result = run_sgv(state["task_content"], cvss_estimate)
    state.update({"sgv_passed": result["passed"], "sgv_feedback": result["feedback"]})

    if state.get("history"):
        state["history"][-1]["sgv_eval"] = result

    if not result["passed"]:
        logger.info("SGV check failed (formal, no GT): %s", result["feedback"])
    return state


def _route_after_sgv(state: ExperimentState) -> str:
    if not state.get("sgv_passed", True) and state["attempts"] < MAX_RETRIES:
        logger.info(
            "SGV verdict=fail → retry attempt %d/%d (formal reason, independent of rubric)",
            state["attempts"] + 1,
            MAX_RETRIES,
        )
        return "retry"
    return "check_answer"


def _check_answer(state: ExperimentState) -> ExperimentState:
    if state["task_type"] == "math":
        verdict, delta, note = _check_math_answer(
            agent_answer=state["final_answer"],
            ground_truth=state["ground_truth"],
        )
        math_judge_score = {"verdict": verdict, "delta": delta, "note": note}
        if state.get("history"):
            state["history"][-1]["judge_score"] = math_judge_score
            state["history"][-1]["verdict"] = verdict
        state.update({"verdict": verdict, "judge_score": math_judge_score})
        return state

    rubric = state.get("rubric", {})
    judge_model, judge_is_hosted = resolve_model_config("judge")
    judge_t0 = time.perf_counter()
    judge_score, j_in_tok, j_out_tok = run_judge_textual(
        task_content=state["task_content"],
        rubric=rubric,
        agent_response=state["final_answer"],
        system_prompt=build_judge_prompt(rubric),
        model=judge_model,
        temperature=config.TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        is_hosted=judge_is_hosted,
    )
    judge_score["judge_elapsed_seconds"] = round(time.perf_counter() - judge_t0, 2)
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

    if state.get("history"):
        state["history"][-1]["judge_score"] = judge_score
        state["history"][-1]["verdict"] = verdict

    state.update({"verdict": verdict, "judge_score": judge_score})
    return state


def _save_result(state: ExperimentState) -> ExperimentState:
    finished_at = datetime.now(timezone.utc).isoformat()
    start_perf = state.get("start_perf")
    elapsed_seconds = time.perf_counter() - start_perf if start_perf is not None else None

    # Blocco B: deterministic CVSS evaluation on vuln tasks (never affects verdict).
    cvss_eval = None
    if config.CVSS_ESTIMATE_ENABLED and is_cvss_task(state["task_id"], state["task_type"]):
        try:
            cvss_eval = evaluate_cvss_estimate(
                state["task_id"], state["final_answer"].get("cvss_estimate")
            )
        except Exception:
            logger.exception("CVSS evaluation failed for %s — recorded as null", state["task_id"])

    rep_payload = {
        # --- repetition index ---
        "repetition": state["repetition"],
        # Tags this repetition with the main.py invocation that produced it —
        # independent of folder naming, so a "run" stays identifiable even
        # when saved alongside other runs under the same role folder.
        "run_id": state.get("run_id"),
        # --- timing ---
        "started_at": state.get("started_at"),
        "finished_at": finished_at,
        "elapsed_seconds": elapsed_seconds,
        # --- agent ---
        "attempts": state["attempts"],
        "history": state["history"],
        # final_answer: clean field view of history[-1] for quick access without full history traversal
        "final_answer": {k: state["final_answer"][k] for k in ("answer", "reasoning", "confidence", "cvss_estimate") if k in state["final_answer"]},
        # --- judge ---
        "verdict": state["verdict"],
        "judge_score": state.get("judge_score", {}),
        # --- CVSS (Blocco B, deterministic — separate from judge_score) ---
        "cvss_eval": cvss_eval,
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
    slug = _model_slug(state["model"], state.get("is_hosted", False))
    result_file = out_dir / f"{slug}.json"

    if result_file.exists():
        try:
            existing = json.loads(result_file.read_text(encoding="utf-8"))
        except Exception:
            existing = None
    else:
        existing = None

    if existing and "repetitions" in existing:
        existing["repetitions"].append(rep_payload)
        payload = existing
    else:
        payload = {
            # --- run config (common across all repetitions) ---
            "task_id": state["task_id"],
            "task_type": state["task_type"],
            "experiment_id": state["experiment_id"],
            "agent_role": state["agent_role"],
            "model": state["model"],
            "judge_model": resolve_model_config("judge")[0],
            "temperature": config.TEMPERATURE,
            "is_hosted": state.get("is_hosted", False),
            "task_path": state["task_path"],
            "sol_path": state["sol_path"],
            "repetitions": [rep_payload],
        }

    result_file.write_text(json.dumps(payload, indent=2, ensure_ascii=True))
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
    graph.add_node("check_sgv", _check_sgv)
    graph.add_node("check_answer", _check_answer)
    graph.add_node("save_result", _save_result)

    graph.set_entry_point("load_task")
    graph.add_edge("load_task", "run_agent")
    graph.add_edge("run_agent", "check_sgv")
    graph.add_conditional_edges(
        "check_sgv", _route_after_sgv, {"retry": "run_agent", "check_answer": "check_answer"}
    )
    graph.add_conditional_edges(
        "check_answer", _route_after_check, {"retry": "run_agent", "save": "save_result"}
    )
    graph.add_edge("save_result", END)

    return graph.compile()
