import argparse
import json
import logging
import re
import signal
import time
from contextlib import contextmanager
from datetime import datetime, timezone
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
    TASK_TIMEOUT_SECONDS,
    TASKS_PATH,
    TEMPERATURE,
    TEXTUAL_PASS_RATIO,
)
from core.checker import check_math_answer
from core.loop_controller import should_retry
from core.result_writer import write_result


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
            "| role | total | correct | accuracy | avg_attempts | avg_textual_score | avg_math_delta |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        breakdown_lines = [
            "",
            "## Task breakdown",
            "",
            "| role | task_id | total | correct | accuracy |",
            "| --- | --- | --- | --- | --- |",
        ]

        for role, payloads in sorted(roles.items()):
            total = len(payloads)
            correct = sum(1 for p in payloads if p.get("verdict") == "correct")
            accuracy = (correct / total) if total else None
            avg_attempts = _avg([float(p.get("attempts", 0)) for p in payloads])

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
                "| {role} | {total} | {correct} | {accuracy} | {avg_attempts} | {avg_textual} | {avg_delta} |".format(
                    role=role,
                    total=total,
                    correct=correct,
                    accuracy=_format_ratio(accuracy),
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

        return "\n".join(lines + breakdown_lines) + "\n"

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
        allowed = set(args.tasks)
        tasks = [task for task in tasks if task.stem in allowed]
        if not tasks:
            raise ValueError("No tasks matched the provided filters")

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

    consistency_lines: List[str] = []

    for experiment in experiments:
        logger.info(
            "Experiment %s | role=%s | model=%s",
            experiment["id"],
            experiment["role"],
            experiment["model"],
        )
        for task_path in tasks:
            logger.info("Task %s", task_path.stem)
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


if __name__ == "__main__":
    main()
