"""Entry point and orchestration; task parsing and evaluation helpers live in utils."""

import argparse
import logging
import time
from datetime import datetime, timezone
from typing import List, Optional

import config
from config import MODELS, REPETITIONS, RESULTS_PATH, TASK_TIMEOUT_SECONDS, TASKS_PATH
from utils.evaluation_utils import _record_consistency_finding, _write_evaluation_reports
from utils.experiment_utils import ExperimentState, _build_graph, _time_limit
from utils.task_utils import _answers_equal, _list_tasks, _result_exists


logger = logging.getLogger(__name__)


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
