"""Entry point and orchestration; task parsing and evaluation helpers live in utils."""

from dotenv import load_dotenv
load_dotenv()

import argparse
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import config
from agents._llm_utils import resolve_model_config
from config import FULL_TASK_SUFFIX, FULL_TASK_TIMEOUT_MULTIPLIER, MODELS, OLLAMA_BASE_URL, REPETITIONS, RESULTS_PATH, TASK_TIMEOUT_SECONDS, TASKS_PATH
from agents._llm_utils import LLMTimeout
from utils.dynamic_task import (
    build_dynamic_tasks,
    discover_source_files,
    is_candidate,
    load_gtfree_rubric,
)
from utils.git_diff import GitSelectionError, changed_files, describe_range
from utils import sast_ingest
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


def _select_source_files(source_dir: str, changed_since: Optional[str]) -> List[Path]:
    """Files to review: the whole tree (mode A) or just what a git range touched (mode B).

    Mode B is a selector on top of mode A, not a different pipeline — see
    `utils/git_diff.py` for why the agent still receives the whole file rather
    than the diff hunk.
    """
    root = Path(source_dir)
    if not changed_since:
        return discover_source_files(
            root, config.DYNAMIC_SOURCE_EXTENSIONS, config.DYNAMIC_EXCLUDE_PATTERNS
        )
    try:
        return changed_files(root, changed_since)
    except GitSelectionError as exc:
        logger.error("--changed-since could not be resolved: %s", exc)
        raise SystemExit(1)


def _resolve_sast_alerts(
    source_dir: str,
    files: List[Path],
    report_path: str,
    path_map_path: Optional[str],
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Any]]:
    """Join a frozen SAST report to the files under review.

    Files with no unambiguous path match are resolved by asking the user, one by
    one (`utils/sast_ingest.py`): an unmatched file means the "with SAST" arm
    silently collapses to the baseline for that file, and a comparison corrupted
    that quietly is worse than a run that stops to ask.
    """
    root = Path(source_dir)
    root_abs = root.resolve()
    rel_paths = []
    for path in files:
        resolved = Path(path).resolve()
        if not resolved.is_relative_to(root_abs):
            continue
        rel = str(resolved.relative_to(root_abs))
        if is_candidate(
            rel, config.DYNAMIC_SOURCE_EXTENSIONS, config.DYNAMIC_EXCLUDE_PATTERNS
        ):
            rel_paths.append(rel)
    alerts, fmt, digest = sast_ingest.load_alerts(report_path)
    matched, ambiguous, absent = sast_ingest.match_alerts(alerts, rel_paths)

    path_map: Dict[str, Optional[str]] = {}
    if path_map_path and Path(path_map_path).is_file():
        path_map = sast_ingest.load_path_map(path_map_path)
        preset = sast_ingest.apply_path_map(
            {k: v for k, v in path_map.items() if k in dict.fromkeys(rel_paths)}, alerts
        )
        matched.update(preset)
        known = set(path_map)
        ambiguous = [(rel, cands) for rel, cands in ambiguous if rel not in known]
        absent = [rel for rel in absent if rel not in known]
        logger.info("SAST path map %s applied (%s entries)", path_map_path, len(path_map))

    unresolved = ambiguous + sast_ingest.confirm_absent(
        absent, len({a["path"] for a in alerts})
    )
    if unresolved:
        answers = sast_ingest.resolve_interactively(unresolved, alerts)
        matched.update(sast_ingest.apply_path_map(answers, alerts))
        path_map.update(answers)
        if path_map_path:
            sast_ingest.save_path_map(path_map_path, path_map)

    if not matched:
        logger.error(
            "SAST arm requested but not one reviewed file matched an alert path in %s — "
            "refusing to run: it would be the baseline under a different name.",
            report_path,
        )
        raise SystemExit(1)

    meta = {
        "report": report_path,
        "format": fmt,
        "sha256": digest,
        "alerts_total": len(alerts),
        "files_with_alerts": sum(1 for v in matched.values() if v),
        "files_total": len(rel_paths),
        "files_absent": len(absent),
    }
    return matched, meta


def _build_dynamic_task_specs(
    source_dir: str,
    experiment: Dict[str, Any],
    exhaustive: bool,
    only_files: Optional[List[Path]] = None,
    sast_alerts_by_file: Optional[Dict[str, List[Dict[str, Any]]]] = None,
    sast_tool: str = "SonarQube",
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
        only_files=only_files,
        sast_alerts_by_file=sast_alerts_by_file,
        sast_tool=sast_tool,
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
        "--changed-since",
        dest="changed_since",
        default=None,
        help="Generic mode B: review only the files changed between <ref> and HEAD "
             "(e.g. --changed-since HEAD~1), instead of every file under --source-dir. "
             "The agent still receives the whole file, not the diff hunk. Requires "
             "--source-dir to be inside a git repository. See utils/git_diff.py.",
    )
    parser.add_argument(
        "--sast-report",
        dest="sast_report",
        default=None,
        help="Generic mode: path to a frozen SAST report (project-normalized, gosec or "
             "semgrep JSON) whose alerts get injected per file. Required to run the "
             "'with SAST' arm in generic mode — SAST_HINT_ENABLED alone does nothing "
             "here, it is keyed on the four known static task ids.",
    )
    parser.add_argument(
        "--sast-path-map",
        dest="sast_path_map",
        default=None,
        help="JSON file mapping a path relative to --source-dir to the corresponding "
             "path in the SAST report (null = no alerts for that file). Read if present "
             "and rewritten with whatever gets resolved interactively, so a repeated run "
             "of the same pair never prompts twice.",
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
    diff_range: Optional[str] = None
    sast_meta: Optional[Dict[str, Any]] = None
    for flag, value in (("--changed-since", args.changed_since),
                        ("--sast-report", args.sast_report),
                        ("--sast-path-map", args.sast_path_map)):
        if value and not dynamic_mode:
            logger.error("%s only applies together with --source-dir", flag)
            raise SystemExit(1)
    # Fail loud instead of running the baseline under the SAST arm's name: the
    # static hint path returns early for gtfree tasks (utils/task_utils.py) and
    # is keyed on _TASK_NF_MAP, so in generic mode the env flag alone injects
    # nothing at all and nothing would say so.
    if dynamic_mode and config.SAST_HINT_ENABLED and not args.sast_report:
        logger.error(
            "SAST_HINT_ENABLED=true has no effect in generic mode: the static hint is "
            "keyed on the four known task ids (utils/sast_hint.py::_TASK_NF_MAP). "
            "Pass --sast-report <file> to run the SAST arm on a pointed directory, or "
            "unset SAST_HINT_ENABLED to run the baseline deliberately."
        )
        raise SystemExit(1)

    if dynamic_mode:
        exhaustive = (
            args.exhaustive_prompt
            if args.exhaustive_prompt is not None
            else config.DYNAMIC_EXHAUSTIVE_PROMPT
        )
        selected = _select_source_files(args.source_dir, args.changed_since)
        if args.changed_since:
            try:
                diff_range = describe_range(Path(args.source_dir), args.changed_since)
            except GitSelectionError:
                diff_range = f"{args.changed_since}..HEAD"
            if not selected:
                # The normal case in a perception loop: nothing relevant moved.
                logger.info(
                    "No file under %s changed in %s — nothing to review.",
                    args.source_dir, diff_range,
                )
                return
        sast_alerts_by_file = None
        if args.sast_report:
            sast_alerts_by_file, sast_meta = _resolve_sast_alerts(
                args.source_dir, selected, args.sast_report, args.sast_path_map
            )
        tasks, not_analyzed = _build_dynamic_task_specs(
            args.source_dir,
            experiments[0],
            exhaustive,
            only_files=selected,
            sast_alerts_by_file=sast_alerts_by_file,
            sast_tool=sast_ingest.TOOL_LABEL.get(
                (sast_meta or {}).get("format", ""), "a static analyzer"
            ),
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
                            "sast_alerts": spec.get("sast_alerts"),
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
                diff_range=diff_range,
                sast_meta=sast_meta,
            )
    else:
        logger.info("Writing evaluation reports")
        executed_tasks = [spec["task_id"] for spec in tasks] if tasks else None
        executed_experiment_ids = list(dict.fromkeys(exp["id"] for exp in experiments))
        _write_evaluation_reports(RESULTS_PATH, task_filter=executed_tasks, experiment_ids=executed_experiment_ids)
    logger.info("Execution complete")


if __name__ == "__main__":
    main()
