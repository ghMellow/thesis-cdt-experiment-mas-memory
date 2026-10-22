"""Inventory of saved repetitions under results/rawJson/, read-only.

For every <task>/<experiment_id>/<role>/<model>.json it lists the repetition
numbers present, the ones missing to reach --target, the run_ids with their
dates, and the mean cost per repetition (wall time, attempts, judge time,
tokens when the provider returned them).

With --check-prompt it also rebuilds, without calling any LLM, the first-attempt
prompt the code of today would send for each candidate configuration (no SAST,
SonarQube, 3-tool, 3-tool + linked code, with/without the NF-context hint) and
says which one matches the `prompt_user` / `prompt_system` saved in each
repetition. A missing repetition can only be added "in the same configuration"
when today's code reproduces the saved prompt byte for byte.

Usage:
    poetry run python -m utils.repetition_inventory [--target 10] [--check-prompt] [--json out.json]
"""

import argparse
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "results" / "rawJson"

# Static CVE tasks (docs/tasks/task5..9). Everything else under rawJson/ comes
# from the generic mode (--source-dir) and is listed apart.
CVE_TASK_PREFIXES = ("task5_", "task6_", "task7_", "task8_", "task9_")

# The hosted (OpenAI-compatible) endpoint returns no prompt_eval_count/eval_count,
# so tokens_in/out are None in every hosted run: token cost is estimated from
# the saved text with the same proxy the generic mode uses (config.DYNAMIC_CHARS_PER_TOKEN).
CHARS_PER_TOKEN = 4.0

SAST_DATASETS = {
    "sonarqube": "docs/sast_tools/ground_truth_vuln_files.json",
    "3tool": "docs/sast_tools/analisi_statica_v4.2.1/hint_alerts_3tool.json",
    "3tool_linked": "docs/sast_tools/analisi_statica_v4.2.1/hint_alerts_3tool_linked.json",
}


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _mean(values: List[float]) -> Optional[float]:
    values = [v for v in values if isinstance(v, (int, float))]
    return round(statistics.mean(values), 1) if values else None


def _first_attempt(rep: Dict[str, Any]) -> Dict[str, Any]:
    history = rep.get("history") or []
    return history[0] if history else {}


def scan(target: int) -> List[Dict[str, Any]]:
    rows = []
    for path in sorted(RAW.glob("*/*/*/*.json")):
        task_id, exp_id, role = path.parts[-4], path.parts[-3], path.parts[-2]
        data = json.loads(path.read_text(encoding="utf-8"))
        reps = data.get("repetitions", [])
        numbers = sorted(r.get("repetition") for r in reps if r.get("repetition") is not None)
        runs: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"reps": [], "dates": set()})
        for r in reps:
            run = runs[r.get("run_id") or "(none)"]
            run["reps"].append(r.get("repetition"))
            if r.get("started_at"):
                run["dates"].add(r["started_at"][:10])
        judge_s, tok_in, tok_out = [], [], []
        est_agent_in, est_agent_out, est_judge_in = [], [], []
        for r in reps:
            a_in = a_out = j_in = 0
            for attempt in r.get("history") or []:
                prompt = len(attempt.get("prompt_system") or "") + len(attempt.get("prompt_user") or "")
                answer = sum(
                    len(json.dumps(attempt.get(k), ensure_ascii=False))
                    for k in ("answer", "reasoning", "cvss_estimate", "native_thinking") if attempt.get(k)
                )
                a_in += prompt
                a_out += answer
                # The judge reads the task body (no retry addendum), the rubric
                # and the answer: approximated by the first-attempt prompt.
                first_user = len(((r.get("history") or [{}])[0]).get("prompt_user") or "")
                j_in += first_user + answer
            est_agent_in.append(a_in / CHARS_PER_TOKEN)
            est_agent_out.append(a_out / CHARS_PER_TOKEN)
            est_judge_in.append(j_in / CHARS_PER_TOKEN)
            for attempt in r.get("history") or []:
                js = (attempt.get("judge_score") or {}).get("judge_elapsed_seconds")
                if js is not None:
                    judge_s.append(js)
                if attempt.get("tokens_in") is not None:
                    tok_in.append(attempt["tokens_in"])
                if attempt.get("tokens_out") is not None:
                    tok_out.append(attempt["tokens_out"])
        n_attempts = [r.get("attempts") for r in reps]
        rows.append({
            "task_id": task_id,
            "experiment_id": exp_id,
            "role": role,
            "model_file": path.name,
            "model": data.get("model"),
            "cve_task": task_id.startswith(CVE_TASK_PREFIXES),
            "temperature": data.get("temperature"),
            "n": len(reps),
            "repetitions": numbers,
            "duplicates": sorted(k for k, v in Counter(numbers).items() if v > 1),
            "missing": [i for i in range(1, target + 1) if i not in numbers],
            "runs": {
                rid: {"reps": sorted(v["reps"]), "dates": sorted(v["dates"])}
                for rid, v in sorted(runs.items())
            },
            "elapsed_mean_s": _mean([r.get("elapsed_seconds") for r in reps]),
            "elapsed_max_s": max((r.get("elapsed_seconds") or 0 for r in reps), default=None),
            "attempts_mean": _mean(n_attempts),
            "attempts_total": sum(a or 0 for a in n_attempts),
            "judge_s_per_attempt": _mean(judge_s),
            "tokens_in_per_attempt": _mean(tok_in),
            "tokens_out_per_attempt": _mean(tok_out),
            "est_tok_agent_in_per_rep": _mean(est_agent_in),
            "est_tok_agent_out_per_rep": _mean(est_agent_out),
            "est_tok_judge_in_per_rep": _mean(est_judge_in),
            "path": str(path.relative_to(ROOT)),
            "_reps": reps,
        })
    return rows


def _candidate_prompts(task_id: str) -> Dict[str, str]:
    """First-attempt user prompt today's code builds, per candidate config."""
    sys.path.insert(0, str(ROOT))
    import config
    from utils.task_utils import _load_task

    task_path = ROOT / config.TASKS_PATH / f"{task_id}.md"
    if not task_path.exists():
        return {}
    sol_path = task_path.with_name(task_id + "_sol.md")
    saved = (config.SAST_HINT_ENABLED, config.SAST_HINT_DATASET_PATH, config.CVSS_CONTEXT_HINT_ENABLED)
    out = {}
    try:
        for ctx in (True, False):
            for arm in ("none", *SAST_DATASETS):
                config.CVSS_CONTEXT_HINT_ENABLED = ctx
                config.SAST_HINT_ENABLED = arm != "none"
                config.SAST_HINT_DATASET_PATH = str(ROOT / SAST_DATASETS.get(arm, saved[1]))
                state = _load_task({"task_path": str(task_path), "sol_path": str(sol_path)})
                label = arm + ("" if ctx else "+no_ctx_hint")
                out[label] = state["task_content"]
    finally:
        config.SAST_HINT_ENABLED, config.SAST_HINT_DATASET_PATH, config.CVSS_CONTEXT_HINT_ENABLED = saved
    return out


def check_prompts(rows: List[Dict[str, Any]]) -> None:
    sys.path.insert(0, str(ROOT))
    from agents.prompts import SYSTEM_PROMPTS

    cache: Dict[str, Dict[str, str]] = {}
    for row in rows:
        if not row["cve_task"]:
            continue
        if row["task_id"] not in cache:
            cache[row["task_id"]] = _candidate_prompts(row["task_id"])
        candidates = cache[row["task_id"]]
        by_hash = defaultdict(list)
        for label, text in candidates.items():
            by_hash[_sha(text)].append(label)
        system_today = SYSTEM_PROMPTS.get(row["role"], "")
        user_match, system_match = Counter(), Counter()
        for rep in row["_reps"]:
            first = _first_attempt(rep)
            user = first.get("prompt_user")
            if user is None:
                user_match["(not saved)"] += 1
            else:
                labels = by_hash.get(_sha(user))
                user_match["=".join(labels) if labels else f"NO MATCH ({_sha(user)})"] += 1
            system = first.get("prompt_system")
            if system is None:
                system_match["(not saved)"] += 1
            else:
                system_match["same" if system == system_today else "DIFFERENT"] += 1
        row["prompt_user_match"] = dict(user_match)
        row["prompt_system_match"] = dict(system_match)


def _fmt_reps(numbers: List[int]) -> str:
    if not numbers:
        return "—"
    spans, start, prev = [], numbers[0], numbers[0]
    for n in numbers[1:] + [None]:
        if n is not None and n == prev + 1:
            prev = n
            continue
        spans.append(str(start) if start == prev else f"{start}-{prev}")
        if n is not None:
            start = prev = n
    return ",".join(spans)


def print_markdown(rows: List[Dict[str, Any]], target: int, prompt: bool) -> None:
    for cve, title in ((True, "CVE tasks (docs/tasks)"), (False, "Generic mode (--source-dir), listed apart")):
        sel = [r for r in rows if r["cve_task"] == cve]
        if not sel:
            continue
        print(f"\n### {title}\n")
        head = "| task | experiment-id | n | reps | missing to {t} | runs (run_id: reps, date) | s/rep mean (max) | attempts/rep | judge s/attempt |".format(t=target)
        if prompt and cve:
            head += " prompt_user first attempt | prompt_system |"
        print(head)
        print("|" + "---|" * (head.count("|") - 1))
        for r in sel:
            runs = "; ".join(
                f"`{rid}`: {_fmt_reps(v['reps'])} ({','.join(v['dates'])})" for rid, v in r["runs"].items()
            )
            line = (
                f"| {r['task_id']} | `{r['experiment_id']}` | {r['n']} | {_fmt_reps(r['repetitions'])}"
                f"{' DUP ' + str(r['duplicates']) if r['duplicates'] else ''} | "
                f"{len(r['missing'])} ({_fmt_reps(r['missing'])}) | {runs} | "
                f"{r['elapsed_mean_s']} ({round(r['elapsed_max_s'] or 0)}) | {r['attempts_mean']} | "
                f"{r['judge_s_per_attempt']} |"
            )
            if prompt and cve:
                um = ", ".join(f"{k}×{v}" for k, v in r.get("prompt_user_match", {}).items())
                sm = ", ".join(f"{k}×{v}" for k, v in r.get("prompt_system_match", {}).items())
                line += f" {um} | {sm} |"
            print(line)
    print(f"\n### Cost of the missing repetitions (target {target}), from the saved ones\n")
    print("| task | experiment-id | missing | s/rep mean | est. time (min) | est. tok/rep (agent in+out, judge in) | est. tok total (k) |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        if not r["missing"]:
            continue
        per_rep = sum(r[k] or 0 for k in ("est_tok_agent_in_per_rep", "est_tok_agent_out_per_rep", "est_tok_judge_in_per_rep"))
        print(
            f"| {r['task_id']} | `{r['experiment_id']}` | {len(r['missing'])} | {r['elapsed_mean_s']} | "
            f"{round(len(r['missing']) * (r['elapsed_mean_s'] or 0) / 60, 1)} | "
            f"{round(r['est_tok_agent_in_per_rep'] or 0)}+{round(r['est_tok_agent_out_per_rep'] or 0)}, "
            f"{round(r['est_tok_judge_in_per_rep'] or 0)} | {round(len(r['missing']) * per_rep / 1000)} |"
        )
    tok = [r for r in rows if r["tokens_in_per_attempt"] is not None]
    print(f"\nRows with token counts saved: {len(tok)}/{len(rows)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--target", type=int, default=10, help="Repetitions each experiment-id should reach")
    parser.add_argument("--check-prompt", action="store_true", help="Compare saved prompts with today's code (no LLM)")
    parser.add_argument("--json", dest="json_out", help="Also write the inventory as JSON here")
    args = parser.parse_args()

    rows = scan(args.target)
    if args.check_prompt:
        check_prompts(rows)
    print_markdown(rows, args.target, args.check_prompt)
    if args.json_out:
        clean = [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]
        Path(args.json_out).write_text(json.dumps(clean, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
