"""Entry point and orchestration; task parsing and evaluation helpers live in utils."""

from dotenv import load_dotenv
load_dotenv()

import argparse
import logging
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import config
from agents._llm_utils import resolve_model_config
from config import FULL_TASK_SUFFIX, FULL_TASK_TIMEOUT_MULTIPLIER, MODELS, OLLAMA_BASE_URL, REPETITIONS, RESULTS_PATH, TASK_TIMEOUT_SECONDS, TASKS_PATH
from utils.evaluation_utils import _record_consistency_finding, _write_evaluation_reports
from utils.experiment_utils import ExperimentState, _build_graph, _fetch_model_context_window, _time_limit
from utils.task_utils import _answers_equal, _list_tasks, _result_exists


logger = logging.getLogger(__name__)


class _SpinnerClearHandler(logging.StreamHandler):
    """Clears the spinner's in-place line before writing each log record."""
    _CLEAR = "\r" + " " * 80 + "\r"

    def emit(self, record: logging.LogRecord) -> None:
        self.stream.write(self._CLEAR)
        super().emit(record)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run multi-agent experiments")
    parser.add_argument(
        "--experiment",
        choices=["1A", "1B", "all"],
        default="all",
        help="Select experiment group",
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
    parser.add_argument(
        "--experiment-id",
        dest="experiment_id",
        default=None,
        help="Override the results folder name (e.g. framing_A1). Model config still resolved from --experiment.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Override generation temperature (default: value from config.py)",
    )
    parser.add_argument(
        "--export-graph",
        dest="export_graph",
        help="Export LangGraph to a PNG file and exit",
    )
    args = parser.parse_args()

    handler = _SpinnerClearHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S"))
    logging.basicConfig(level=logging.INFO, handlers=[handler])

    if args.temperature is not None:
        config.TEMPERATURE = args.temperature

    graph = _build_graph()
    if args.export_graph:
        graph.get_graph().draw_mermaid_png(output_file_path=args.export_graph)
        logger.info("LangGraph exported to %s", args.export_graph)
        return
    tasks = _list_tasks(TASKS_PATH)
    if args.tasks:
        available = {task.stem for task in tasks}
        requested = set(args.tasks)
        missing = sorted(requested - available)
        if missing:
            logger.error("Unknown task ids: %s", ", ".join(missing))
            raise SystemExit(1)
        tasks = [task for task in tasks if task.stem in requested]

    experiments = []
    for exp_id in ["1A", "1B"]:
        model, is_hosted = resolve_model_config(f"agent_{exp_id}")
        experiments.append({"id": exp_id, "role": "agent", "model": model, "is_hosted": is_hosted})
    if args.experiment != "all":
        experiments = [exp for exp in experiments if exp["id"] == args.experiment]
    if not experiments:
        raise ValueError("No experiments matched the provided filters")
    if args.experiment_id:
        for exp in experiments:
            exp["id"] = args.experiment_id

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
                    experiment["model"],
                    experiment["is_hosted"],
                ):
                    continue
                remaining_repetitions += 1

    # If any task in the run has FULL_TASK_SUFFIX in its name, it gets a higher timeout;
    # bump OLLAMA_TIMEOUT_SECONDS now so it covers the worst-case full-task timeout.
    has_full_task = any(FULL_TASK_SUFFIX in t.stem for t in tasks) if args.task_timeout > 0 else False
    max_effective_timeout = int(args.task_timeout * FULL_TASK_TIMEOUT_MULTIPLIER) if has_full_task else args.task_timeout
    desired_ollama_timeout = int(max_effective_timeout * 1.1)
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

    ctx_cache: Dict[str, Any] = {}

    for experiment in experiments:
        model = experiment["model"]
        if model not in ctx_cache:
            ctx_cache[model] = None if experiment["is_hosted"] else _fetch_model_context_window(model, OLLAMA_BASE_URL)
        ctx_window = ctx_cache[model]
        ctx_str = f" | ctx_window={ctx_window:,}" if ctx_window else ""
        logger.info("")
        hosted_str = " [hosted]" if experiment["is_hosted"] else ""
        logger.info(
            "==== Experiment %s | role=%s | model=%s%s%s ====",
            experiment["id"],
            experiment["role"],
            model,
            hosted_str,
            ctx_str,
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
                    experiment["model"],
                    experiment["is_hosted"],
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
                    "is_hosted": experiment["is_hosted"],
                    "attempts": 0,
                    "history": [],
                    "experiment_id": experiment["id"],
                    "repetition": repetition,
                    "started_at": started_at,
                    "start_perf": start_perf,
                }
                # Tasks with FULL_TASK_SUFFIX in the name get an extended timeout
                # because their prompts are much larger and each LLM call takes proportionally longer.
                effective_timeout = args.task_timeout
                if args.task_timeout > 0 and FULL_TASK_SUFFIX in task_path.stem:
                    effective_timeout = int(args.task_timeout * FULL_TASK_TIMEOUT_MULTIPLIER)
                    logger.info(
                        "Full task detected ('%s') → timeout %ss → %ss",
                        FULL_TASK_SUFFIX, args.task_timeout, effective_timeout,
                    )
                try:
                    with _time_limit(effective_timeout):
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
    executed_tasks = [task_path.stem for task_path in tasks] if tasks else None
    executed_experiment_ids = list(dict.fromkeys(exp["id"] for exp in experiments))
    _write_evaluation_reports(RESULTS_PATH, task_filter=executed_tasks, experiment_ids=executed_experiment_ids)
    logger.info("Execution complete")


if __name__ == "__main__":
    main()
