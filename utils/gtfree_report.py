"""Minimal Markdown report for GT-free runs (--source-dir, no ground truth).

The regular reports (`utils/evaluation_utils.py::_write_evaluation_reports`)
are built around the known-CVE dataset: detection rate, precision@k, TP/FP
variability, CVE×repetition matrices — every one of them needs a reference
answer to compare against, and on an arbitrary source file there is none.

What survives without ground truth, and is what this report shows:

- the **findings themselves** — on a GT-free run every finding is by definition
  unmatched/new, so the inventory *is* the result, not a leftover bucket;
- **repetition stability** — the same file analyzed N times: which findings come
  back every time and which appear once. Cheap proxy for confidence that needs
  no reference answer (a finding reported 3/3 times is not necessarily true, but
  a 1/3 one is measurably unstable);
- **rubric v2 scores per criterion** — where the report loses points (evidence,
  absence claims, granularity, classification, severity);
- **SGV**, deterministic and GT-free by construction;
- **cost** (tokens, wall clock).

What it deliberately does NOT report, and says so in the output: completeness.
Whether the model missed something requires knowing what is there — that needs
the external candidate enumerator (G5/SAST), never built. See
docs/generalizzazione/00_costruzione_dinamica_task.md.
"""

import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from config import REPORTS_PATH
from utils.dynamic_task import load_gtfree_rubric
from utils.evaluation_utils import (
    _avg,
    _build_cost_metrics_section,
    _build_run_id_note,
    _build_sgv_section,
    _collect_results,
    _fmt,
    _fmt_ratio,
    _normalize_function_name,
    _retry_cause,
)

logger = logging.getLogger(__name__)


def _findings_of(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    estimate = (payload.get("final_answer") or {}).get("cvss_estimate")
    if not isinstance(estimate, dict):
        return []
    findings = estimate.get("findings")
    return [f for f in findings if isinstance(f, dict)] if isinstance(findings, list) else []


def _sgv_status_by_function(payload: Dict[str, Any]) -> Dict[str, str]:
    """Last attempt's per-finding SGV outcome, keyed by normalized function."""
    history = payload.get("history") or []
    if not history:
        return {}
    sgv = history[-1].get("sgv_eval")
    if not isinstance(sgv, dict):
        return {}
    out: Dict[str, str] = {}
    for pf in sgv.get("per_finding", []) or []:
        key = _normalize_function_name(pf.get("function"))
        if pf.get("passed", True):
            out[key] = "ok"
        else:
            bad = "; ".join(f"{k}: {v}" for k, v in (pf.get("checks") or {}).items() if v != "ok")
            out[key] = bad or "fail"
    return out


def _jaccard(a: set, b: set) -> Optional[float]:
    union = a | b
    return len(a & b) / len(union) if union else None


def _by_task(payloads: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for p in payloads:
        if p.get("task_id"):
            grouped[p["task_id"]].append(p)
    return dict(sorted(grouped.items()))


def _build_files_table(payloads: List[Dict[str, Any]]) -> List[str]:
    lines = [
        '<a id="files"></a>',
        "## Files analyzed",
        "",
        "| task_id | source file | reps | correct | mean rubric (0–1) | mean attempts | findings/rep |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for task_id, reps in _by_task(payloads).items():
        norms = [
            float(r["judge_score"]["normalized_score"])
            for r in reps
            if isinstance((r.get("judge_score") or {}).get("normalized_score"), (int, float))
        ]
        n_correct = sum(1 for r in reps if r.get("verdict") == "correct")
        n_findings = _avg([float(len(_findings_of(r))) for r in reps])
        lines.append(
            f"| `{task_id}` | `{reps[0].get('task_path', '')}` | {len(reps)} | "
            f"{n_correct}/{len(reps)} | {_fmt(_avg(norms), 3)} | "
            f"{_fmt(_avg([float(r.get('attempts', 1)) for r in reps]), 2)} | "
            f"{_fmt(n_findings, 1)} |"
        )
    lines += [
        "",
        "**Legend** — `correct` here means the GT-free rubric score cleared "
        "`config.TEXTUAL_PASS_RATIO`, i.e. the report is *well-formed and grounded*, "
        "**not** that the vulnerability it describes is real. Without ground truth "
        "there is nothing in this run that can say the latter.",
        "",
    ]
    return lines


def _build_rubric_breakdown(payloads: List[Dict[str, Any]]) -> List[str]:
    """Mean score per rubric criterion — shows which criterion costs points.

    The rubric itself is not persisted in the result JSON (it is run config, not
    output), so the criteria and their maxima are read back from the rubric file
    the run used. That list also acts as the whitelist: `judge_score` carries
    derived fields (`total_score`, `normalized_score`) that are not criteria.
    """
    import config

    try:
        rubric_items = load_gtfree_rubric(config.DYNAMIC_RUBRIC_PATH).get("rubrica", {})
    except FileNotFoundError:
        rubric_items = {}
    maxima = {field: float(spec.get("max", 0)) for field, spec in rubric_items.items()}

    per_field: Dict[str, List[float]] = defaultdict(list)
    for p in payloads:
        js = p.get("judge_score") or {}
        for field in maxima:
            value = js.get(field)
            if isinstance(value, (int, float)):
                per_field[field].append(float(value))
    if not per_field:
        return []
    lines = [
        '<a id="rubric"></a>',
        "## Rubric v2 (GT-free) — mean score per criterion",
        "",
        "| criterion | mean | max | ratio |",
        "| --- | --- | --- | --- |",
    ]
    for field in sorted(per_field, key=lambda f: _avg(per_field[f]) / (maxima.get(f) or 1)):
        mean = _avg(per_field[field])
        max_val = maxima.get(field)
        ratio = (mean / max_val) if (mean is not None and max_val) else None
        lines.append(
            f"| `{field}` | {_fmt(mean, 2)} | {max_val:.0f} | {_fmt_ratio(ratio)} |"
        )
    lines += [
        "",
        "Sorted worst-first by ratio: the top row is where the reports lose the most. "
        "Rubric: `config.DYNAMIC_RUBRIC_PATH`.",
        "",
    ]
    return lines


def _build_findings_inventory(payloads: List[Dict[str, Any]]) -> List[str]:
    """Every finding produced by the run, grouped per file and function.

    On a GT-free run this is the actual output: there is no matched/unmatched
    split to make, so nothing is filtered out. `seen` = in how many repetitions
    of that file the same function was flagged — the only stability signal
    available without a reference answer.
    """
    lines = ['<a id="findings"></a>', "## Findings inventory", ""]
    total = 0
    for task_id, reps in _by_task(payloads).items():
        n_reps = len(reps)
        grouped: Dict[str, Dict[str, Any]] = {}
        for rep in reps:
            sgv_status = _sgv_status_by_function(rep)
            for finding in _findings_of(rep):
                key = _normalize_function_name(finding.get("function"))
                entry = grouped.setdefault(
                    key,
                    {
                        "function": finding.get("function"),
                        "reps": set(),
                        "scores": [],
                        "vectors": set(),
                        "snippets": set(),
                        "sgv": set(),
                    },
                )
                entry["reps"].add(rep.get("repetition"))
                if isinstance(finding.get("score"), (int, float)):
                    entry["scores"].append(float(finding["score"]))
                if finding.get("vector"):
                    entry["vectors"].add(str(finding["vector"]))
                if finding.get("snippet"):
                    entry["snippets"].add(str(finding["snippet"]).strip())
                entry["sgv"].add(sgv_status.get(key, "n/a"))

        if not grouped:
            lines += [f"### `{task_id}` — no findings reported", ""]
            continue

        total += len(grouped)
        lines += [
            f"### `{task_id}` ({len(grouped)} distinct function(s) flagged over {n_reps} rep(s))",
            "",
            "| seen | function | CVSS score | SGV | evidence snippet |",
            "| --- | --- | --- | --- | --- |",
        ]
        for entry in sorted(
            grouped.values(),
            key=lambda e: (-len(e["reps"]), -(max(e["scores"]) if e["scores"] else 0)),
        ):
            scores = entry["scores"]
            score_str = (
                f"{min(scores):.1f}–{max(scores):.1f}" if len(set(scores)) > 1
                else (f"{scores[0]:.1f}" if scores else "n/a")
            )
            snippet = sorted(entry["snippets"])[0] if entry["snippets"] else ""
            snippet = snippet.replace("|", "\\|")
            if len(snippet) > 90:
                snippet = snippet[:87] + "..."
            sgv = "; ".join(sorted(s for s in entry["sgv"] if s != "n/a")) or "n/a"
            lines.append(
                f"| {len(entry['reps'])}/{n_reps} | `{entry['function']}` | {score_str} | "
                f"{sgv} | `{snippet}` |"
            )
        lines.append("")

    if total == 0:
        return []
    lines += [
        "**Legend**",
        "",
        "- `seen` = repetitions of that file in which the same function was flagged. "
        "A 1/3 finding is measurably unstable; a 3/3 one is stable — **stable is not "
        "the same as true**, no ground truth is consulted anywhere in this report.",
        "- `CVSS score` = the agent's own estimate (range shown when it varied across "
        "repetitions), never compared to a reference score here.",
        "- `SGV` = deterministic grounding checks on the last attempt (`ok` = the cited "
        "function and snippet exist in the reviewed file).",
        "- Findings are grouped by function name, so two different weaknesses reported "
        "on the same function collapse into one row — read the raw JSON under "
        "`results/rawJson/<task_id>/` for the full text.",
        "",
    ]
    return lines


def _build_stability_section(payloads: List[Dict[str, Any]]) -> List[str]:
    """Agreement between repetitions on *which* functions get flagged."""
    rows: List[str] = []
    for task_id, reps in _by_task(payloads).items():
        if len(reps) < 2:
            continue
        sets = [
            {_normalize_function_name(f.get("function")) for f in _findings_of(r)}
            for r in reps
        ]
        pairwise = [
            j
            for i in range(len(sets))
            for k in range(i + 1, len(sets))
            if (j := _jaccard(sets[i], sets[k])) is not None
        ]
        always = set.intersection(*sets) if sets else set()
        ever = set.union(*sets) if sets else set()
        rows.append(
            f"| `{task_id}` | {len(reps)} | {_fmt(_avg(pairwise), 2)} | "
            f"{len(always)} | {len(ever)} |"
        )
    if not rows:
        return []
    return [
        '<a id="stability"></a>',
        "## Repetition stability (same file, N runs)",
        "",
        "| task_id | reps | mean Jaccard | flagged in every rep | flagged in at least one |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
        "**Legend** — Jaccard over the *sets of flagged functions* between every pair of "
        "repetitions: 1.00 = the model flags exactly the same functions every time, "
        "0.00 = no overlap at all. The gap between the last two columns is the size of "
        "the unstable perimeter. This replaces the TP/FP variability section of the "
        "GT-based reports, which cannot be computed without a reference answer.",
        "",
    ]


def _build_retry_section(payloads: List[Dict[str, Any]]) -> List[str]:
    """Which gate caused each retry (SGV vs rubric) — counts only.

    The GT-based report also measures the TP/FP delta each retry produced;
    that needs the CVE dataset, so here only the channel counts survive.
    """
    causes: Dict[str, int] = defaultdict(int)
    for p in payloads:
        history = p.get("history") or []
        for attempt in history[:-1]:
            causes[_retry_cause(attempt)] += 1
    if not causes:
        return []
    total = sum(causes.values())
    lines = [
        '<a id="retries"></a>',
        "## Retry channels",
        "",
        "| cause | retries | share |",
        "| --- | --- | --- |",
    ]
    for cause, n in sorted(causes.items(), key=lambda kv: -kv[1]):
        lines.append(f"| {cause} | {n} | {_fmt_ratio(n / total)} |")
    lines += [
        "",
        "Which gate rejected an attempt and sent it back: SGV (deterministic, formal) "
        "or the rubric judge. Unlike the GT-based report, the *effect* of each retry on "
        "detection is not measurable here.",
        "",
    ]
    return lines


def _build_skipped_section(skipped: List[str]) -> List[str]:
    if not skipped:
        return []
    return [
        '<a id="skipped"></a>',
        "## Files not analyzed",
        "",
        *[f"- {item}" for item in skipped],
        "",
        "Skipped by the pre-flight token gate (`config.DYNAMIC_PROMPT_CTX_RATIO`) or "
        "after a timeout. Listed here so the denominator of everything above is honest: "
        "these files were never sent to the model.",
        "",
    ]


def write_gtfree_report(
    results_path: str,
    experiment_id: str,
    task_filter: Optional[List[str]] = None,
    run_id: Optional[str] = None,
    skipped: Optional[List[str]] = None,
    source_dir: Optional[str] = None,
) -> Optional[Path]:
    data = _collect_results(results_path, run_id=run_id)
    roles = data.get(experiment_id, {})
    payloads = [
        {"_role": role, **p}
        for role, role_payloads in roles.items()
        for p in role_payloads
        if p.get("gtfree")
    ]
    if task_filter is not None:
        payloads = [p for p in payloads if p.get("task_id") in task_filter]
    if not payloads and not skipped:
        logger.info("No GT-free results to report for %s", experiment_id)
        return None

    first = payloads[0] if payloads else {}
    lines = [
        f"# GT-free run — {experiment_id}",
        "",
        "Generic mode (`--source-dir`): tasks built in memory from source files, "
        "**no ground truth, no CVE matching**. See "
        "`docs/generalizzazione/00_costruzione_dinamica_task.md`.",
        "",
        "| | |",
        "| --- | --- |",
        f"| source dir | `{source_dir or 'n/a'}` |",
        f"| prompt variant | `{first.get('prompt_variant') or 'n/a'}` "
        f"(`utils/dynamic_task.py::REVIEW_INSTRUCTION_*`) |",
        f"| files analyzed | {len(_by_task(payloads))} |",
        f"| repetitions | {len(payloads)} |",
        f"| agent model | `{first.get('model', 'n/a')}` |",
        f"| judge model | `{first.get('judge_model', 'n/a')}` |",
        f"| temperature | {first.get('temperature', 'n/a')} |",
        "",
    ]
    lines += _build_run_id_note(payloads)
    lines += [
        "> **Not measured here: completeness.** Every section below judges what the "
        "model *did* report. Whether it missed a weakness that is actually in the file "
        "cannot be answered without an external enumerator of candidates (proposal "
        "G5/SAST, never implemented) — declared limit, not an omission.",
        "",
    ]
    lines += _build_files_table(payloads)
    lines += _build_findings_inventory(payloads)
    lines += _build_stability_section(payloads)
    lines += _build_rubric_breakdown(payloads)
    lines += _build_retry_section(payloads)
    lines += _build_sgv_section(payloads)
    lines += _build_cost_metrics_section({"agent": payloads})
    lines += _build_skipped_section(skipped or [])

    out_dir = Path(REPORTS_PATH) / "gtfree"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{experiment_id}.md"
    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("Written %s", out_file)
    return out_file
