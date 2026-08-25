"""Entry point and orchestration; task parsing and evaluation helpers live in utils."""

from dotenv import load_dotenv
load_dotenv()

import argparse
import logging
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import config
from agents._llm_utils import resolve_model_config
from config import FULL_TASK_SUFFIX, FULL_TASK_TIMEOUT_MULTIPLIER, MODELS, OLLAMA_BASE_URL, REPETITIONS, RESULTS_PATH, TASK_TIMEOUT_SECONDS, TASKS_PATH
from agents._llm_utils import LLMTimeout
from utils.dynamic_task import build_dynamic_tasks, load_gtfree_rubric
from utils.gtfree_report import write_gtfree_report
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


def _build_dynamic_task_specs(
    source_dir: str, experiment: Dict[str, Any], exhaustive: bool
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Build one task spec per source file under `source_dir` (generic mode A).

    Sizes the pre-flight token gate against the agent model's context window.
    `_fetch_model_context_window` queries the local Ollama /api/show, so on a
    hosted model there is nothing to query — falls back to the configured
    HOSTED_CONTEXT_WINDOW_FALLBACK (0 disables the gate).
    """
    if experiment["is_hosted"]:
        ctx_window = config.HOSTED_CONTEXT_WINDOW_FALLBACK
        ctx_source = "config.HOSTED_CONTEXT_WINDOW_FALLBACK (hosted model)"
    else:
        ctx_window = _fetch_model_context_window(experiment["model"], OLLAMA_BASE_URL)
        ctx_source = "Ollama /api/show"
        if not ctx_window:
            ctx_window = config.HOSTED_CONTEXT_WINDOW_FALLBACK
            ctx_source = "config.HOSTED_CONTEXT_WINDOW_FALLBACK (/api/show gave nothing)"

    max_prompt_tokens = int(ctx_window * config.DYNAMIC_PROMPT_CTX_RATIO) if ctx_window else None
    if max_prompt_tokens:
        logger.info(
            "Pre-flight token gate: %s tok (%.0f%% of ctx_window=%s from %s)",
            f"{max_prompt_tokens:,}",
            config.DYNAMIC_PROMPT_CTX_RATIO * 100,
            f"{ctx_window:,}",
            ctx_source,
        )
    else:
        logger.warning("Pre-flight token gate disabled (no context window available)")

    return build_dynamic_tasks(
        source_dir=source_dir,
        rubric=load_gtfree_rubric(config.DYNAMIC_RUBRIC_PATH),
        extensions=config.DYNAMIC_SOURCE_EXTENSIONS,
        exclude_patterns=config.DYNAMIC_EXCLUDE_PATTERNS,
        max_prompt_tokens=max_prompt_tokens,
        chars_per_token=config.DYNAMIC_CHARS_PER_TOKEN,
        exhaustive=exhaustive,
    )


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
        "--source-dir",
        dest="source_dir",
        default=None,
        help="Generic mode: point at a directory of source files instead of docs/tasks/. "
             "One file = one task, prompt built in memory (utils/dynamic_task.py), no ground "
             "truth and no CVE matching — judged only by the GT-free rubric v2. "
             "See docs/generalizzazione/00_costruzione_dinamica_task.md.",
    )
    parser.add_argument(
        "--exhaustive-prompt",
        dest="exhaustive_prompt",
        action="store_true",
        default=None,
        help="Dynamic mode only: use the exhaustive review instruction "
             "(read the file in full, no limit on findings) instead of the base one. "
             "Default from config.DYNAMIC_EXHAUSTIVE_PROMPT.",
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
    parser.add_argument(
        "--run-id",
        dest="run_id",
        default=None,
        help="Tag every repetition saved by this invocation with a run id (default: "
             "auto-generated UTC timestamp). Stored in the JSON, not just the folder name — "
             "lets utils.evaluation_utils filter/report on exactly this run later, even if "
             "results land in a folder shared with other runs (e.g. --experiment-id reuse).",
    )
    args = parser.parse_args()
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

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
    # 1B disabilitato (2026-07-13): il progetto ora esegue solo il framing 1A.
    # Per riattivarlo, scommentare "1B" nella lista sottostante.
    experiments = []
    for exp_id in ["1A"]:  # era ["1A", "1B"]
        model, is_hosted = resolve_model_config(f"agent_{exp_id}")
        experiments.append({"id": exp_id, "role": "agent", "model": model, "is_hosted": is_hosted})
    if args.experiment != "all":
        experiments = [exp for exp in experiments if exp["id"] == args.experiment]
    if not experiments:
        raise ValueError("No experiments matched the provided filters")
    if args.experiment_id:
        for exp in experiments:
            exp["id"] = args.experiment_id

    dynamic_mode = bool(args.source_dir)
    not_analyzed: List[str] = []
    if dynamic_mode:
        exhaustive = (
            args.exhaustive_prompt
            if args.exhaustive_prompt is not None
            else config.DYNAMIC_EXHAUSTIVE_PROMPT
        )
        tasks, not_analyzed = _build_dynamic_task_specs(
            args.source_dir, experiments[0], exhaustive
        )
    else:
        tasks = [
            {
                "task_id": path.stem,
                "task_path": str(path),
                "sol_path": str(path.with_name(path.stem + "_sol.md")),
                "gtfree": False,
            }
            for path in _list_tasks(TASKS_PATH)
        ]
    if args.tasks:
        available = {spec["task_id"] for spec in tasks}
        requested = set(args.tasks)
        missing = sorted(requested - available)
        if missing:
            logger.error("Unknown task ids: %s", ", ".join(missing))
            raise SystemExit(1)
        tasks = [spec for spec in tasks if spec["task_id"] in requested]
    if not tasks:
        logger.error("No tasks to run")
        raise SystemExit(1)

    remaining_repetitions = 0
    for experiment in experiments:
        for spec in tasks:
            for repetition in range(1, args.repetitions + 1):
                if _result_exists(
                    RESULTS_PATH,
                    experiment["id"],
                    experiment["role"],
                    spec["task_id"],
                    repetition,
                    experiment["model"],
                    experiment["is_hosted"],
                ):
                    continue
                remaining_repetitions += 1

    # If any task in the run has FULL_TASK_SUFFIX in its name, it gets a higher timeout;
    # bump OLLAMA_TIMEOUT_SECONDS now so it covers the worst-case full-task timeout.
    has_full_task = any(FULL_TASK_SUFFIX in spec["task_id"] for spec in tasks) if args.task_timeout > 0 else False
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
        "run_id=%s | worst-case max time: %s | Ollama timeout: %ss | Remaining repetitions: %s",
        run_id,
        worst_case_hms,
        config.OLLAMA_TIMEOUT_SECONDS,
        remaining_repetitions,
    )

    consistency_lines: List[str] = []
    # Files skipped after a timeout in dynamic mode — reported at the end so a
    # partial batch says explicitly what is missing.
    timed_out: List[str] = []

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
        for spec in tasks:
            task_id = spec["task_id"]
            logger.info("")
            logger.info("---- Task %s ----", task_id)
            previous_answer: Optional[Dict[str, Any]] = None

            for repetition in range(1, args.repetitions + 1):
                if _result_exists(
                    RESULTS_PATH,
                    experiment["id"],
                    experiment["role"],
                    task_id,
                    repetition,
                    experiment["model"],
                    experiment["is_hosted"],
                ):
                    logger.info("Skip %s rep %s (already exists)", task_id, repetition)
                    continue
                logger.info("Repetition %s/%s", repetition, args.repetitions)
                started_at = datetime.now(timezone.utc).isoformat()
                start_perf = time.perf_counter()
                initial_state: ExperimentState = {
                    "task_path": spec["task_path"],
                    "sol_path": spec["sol_path"],
                    "agent_role": experiment["role"],
                    "model": experiment["model"],
                    "is_hosted": experiment["is_hosted"],
                    "attempts": 0,
                    "history": [],
                    "experiment_id": experiment["id"],
                    "repetition": repetition,
                    "started_at": started_at,
                    "start_perf": start_perf,
                    "run_id": run_id,
                }
                if spec["gtfree"]:
                    # Dynamic mode: the task body, id, type and (GT-free) rubric are
                    # carried in the state — utils/task_utils.py:_load_task returns
                    # them untouched instead of reading docs/tasks/.
                    initial_state.update(
                        {
                            "gtfree": True,
                            "task_id": task_id,
                            "task_type": spec["task_type"],
                            "task_content": spec["task_content"],
                            "rubric": spec["rubric"],
                            "prompt_variant": spec["prompt_variant"],
                        }
                    )
                # Tasks with FULL_TASK_SUFFIX in the name get an extended timeout
                # because their prompts are much larger and each LLM call takes proportionally longer.
                effective_timeout = args.task_timeout
                if args.task_timeout > 0 and FULL_TASK_SUFFIX in task_id:
                    effective_timeout = int(args.task_timeout * FULL_TASK_TIMEOUT_MULTIPLIER)
                    logger.info(
                        "Full task detected ('%s') → timeout %ss → %ss",
                        FULL_TASK_SUFFIX, args.task_timeout, effective_timeout,
                    )
                try:
                    with _time_limit(effective_timeout):
                        result_state = graph.invoke(initial_state)
                except (TimeoutError, LLMTimeout) as exc:
                    logger.warning(
                        "Timeout | %s rep %s | %s: %s (task limit %ss)",
                        task_id,
                        repetition,
                        type(exc).__name__,
                        exc,
                        effective_timeout,
                    )
                    if dynamic_mode:
                        # One slow file out of N must not take the whole batch
                        # down: record it and move on to the next repetition/file.
                        timed_out.append(f"{task_id} rep {repetition}")
                        not_analyzed.append(f"`{task_id}` rep {repetition} — timeout")
                        continue
                    logger.error("Exiting after timeout to allow manual restart of Ollama")
                    raise SystemExit(1)
                final_answer = result_state.get("final_answer", {})
                logger.info(
                    "Done %s rep %s | verdict=%s | attempts=%s",
                    result_state.get("task_id", task_id),
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
    if timed_out:
        logger.warning("Timed out and skipped (%s): %s", len(timed_out), ", ".join(timed_out))
    if dynamic_mode:
        # The regular reports (utils/evaluation_utils.py) need the known-CVE
        # dataset for every section they build. The GT-free report keeps only
        # what survives without a reference answer — findings inventory,
        # repetition stability, rubric criteria, SGV, cost — and says in its
        # own text what it cannot measure (completeness).
        logger.info("Writing GT-free report (no ground truth in this mode)")
        for experiment_id in dict.fromkeys(exp["id"] for exp in experiments):
            write_gtfree_report(
                RESULTS_PATH,
                experiment_id,
                task_filter=[spec["task_id"] for spec in tasks],
                run_id=run_id,
                skipped=not_analyzed,
                source_dir=args.source_dir,
            )
    else:
        logger.info("Writing evaluation reports")
        executed_tasks = [spec["task_id"] for spec in tasks] if tasks else None
        executed_experiment_ids = list(dict.fromkeys(exp["id"] for exp in experiments))
        _write_evaluation_reports(RESULTS_PATH, task_filter=executed_tasks, experiment_ids=executed_experiment_ids)
    logger.info("Execution complete")


if __name__ == "__main__":
    main()
