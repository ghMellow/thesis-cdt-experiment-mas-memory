"""Compare agent latency between two experiment-ids of the same task.

Answers "did the hosted model get faster?" from what the runs left on disk,
without any new inference call. Reads
`<RESULTS_PATH>/<task>/<exp>/agent/*.json` for each experiment and reports,
per series (one series = one experiment, and inside it one series per run_id):

- per agent call (each entry of `history`): wall-clock seconds of the LLM call,
  output length in characters (answer + reasoning + CVSS findings serialized),
  characters per second, and prompt length;
- first attempt only: same prompt template on both sides, so it is the cleanest
  like-for-like comparison (retries carry SGV feedback and a longer prompt);
- per repetition: total elapsed (agent + judge + SGV), attempts, judge seconds.

Token counts are printed when present; on hosted runs they are null because
the OpenAI-compatible endpoint does not return Ollama's `prompt_eval_count` /
`eval_count`, so characters per second is the throughput proxy.

Mann-Whitney U (two-sided) is computed when scipy is importable — it is a
transitive dependency here, not a declared one, so its absence only drops the
test, never the descriptives.

Usage:
    poetry run python utils/compare_run_timing.py task6_vuln_udr_full \
        1A_sast_hint_full 1A_sast_hint_full_rerun2610
    poetry run python utils/compare_run_timing.py --all
"""

import argparse
import glob
import json
import os
import statistics
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402

try:
    from scipy.stats import mannwhitneyu
except ImportError:  # pragma: no cover
    mannwhitneyu = None

# Pairs (task, before, after) with both sides on disk, used by --all.
DEFAULT_PAIRS = [
    ("task6_vuln_udr_full", "1A_sast_hint_full", "1A_sast_hint_full_rerun2610"),
    ("task6_vuln_udr_full", "1A_no_hint_full", "1A_no_hint_full_rerun2610"),
    ("task8_vuln_udm_full", "1A_sast_hint_full", "1A_sast_hint_full_rerun2610"),
    ("task8_vuln_udm_full", "1A", "1A_no_hint_full_rerun2610"),
    ("task6_vuln_udr_full", "1A", "1A_no_hint_full_rerun2610"),
]

# Fields that may carry model identity if a future run records them.
MODEL_META_KEYS = ("model", "judge_model", "model_digest", "digest", "system_fingerprint", "model_version")


def _load(task: str, exp: str) -> List[Dict[str, Any]]:
    paths = sorted(glob.glob(os.path.join(config.RESULTS_PATH, task, exp, "agent", "*.json")))
    if not paths:
        raise SystemExit(f"no agent JSON under {config.RESULTS_PATH}{task}/{exp}/agent/")
    return [json.load(open(p)) for p in paths]


def _output_chars(h: Dict[str, Any]) -> int:
    parts = [h.get("answer") or "", h.get("reasoning") or "", h.get("native_thinking") or ""]
    cvss = h.get("cvss_estimate")
    if cvss:
        parts.append(json.dumps(cvss, ensure_ascii=False))
    return sum(len(p) for p in parts)


def _rows(payloads: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Flatten into call-level and repetition-level rows."""
    calls, reps = [], []
    for d in payloads:
        for r in d["repetitions"]:
            hist = r.get("history") or []
            judge_s = sum((h.get("judge_score") or {}).get("judge_elapsed_seconds") or 0 for h in hist)
            final_judge = (r.get("judge_score") or {}).get("judge_elapsed_seconds") or 0
            reps.append({
                "run_id": r.get("run_id"),
                "repetition": r.get("repetition"),
                "elapsed": r.get("elapsed_seconds"),
                "attempts": r.get("attempts"),
                "agent_s": sum(h.get("elapsed_seconds") or 0 for h in hist),
                "judge_s": judge_s + final_judge,
                "tok_agent_out": (r.get("tokens") or {}).get("agent_out"),
            })
            for i, h in enumerate(hist):
                sec = h.get("elapsed_seconds")
                chars = _output_chars(h)
                calls.append({
                    "run_id": r.get("run_id"),
                    "attempt": i + 1,
                    "sec": sec,
                    "out_chars": chars,
                    "chars_per_s": chars / sec if sec else None,
                    "prompt_chars": len(h.get("prompt_user") or "") + len(h.get("prompt_system") or ""),
                    "tok_in": h.get("tokens_in"),
                    "tok_out": h.get("tokens_out"),
                    "tok_per_s": (h["tokens_out"] / sec) if h.get("tokens_out") and sec else None,
                    "native_thinking": bool(h.get("native_thinking")),
                })
    return {"calls": calls, "reps": reps}


def _desc(xs: List[Optional[float]]) -> str:
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return "n=0 (null)"
    if len(xs) >= 4:
        q = statistics.quantiles(xs, n=4)
        iqr = f"IQR [{q[0]:.1f}, {q[2]:.1f}]"
    else:
        iqr = "IQR n/a"
    return f"n={len(xs):>2} med={statistics.median(xs):8.1f} {iqr:<22} min={xs[0]:8.1f} max={xs[-1]:8.1f}"


def _mw(a: List[Optional[float]], b: List[Optional[float]]) -> str:
    a = [x for x in a if x is not None]
    b = [x for x in b if x is not None]
    if mannwhitneyu is None:
        return "Mann-Whitney: scipy non disponibile"
    if len(a) < 2 or len(b) < 2:
        return "Mann-Whitney: n troppo piccolo"
    res = mannwhitneyu(a, b, alternative="two-sided")
    ratio = statistics.median(b) / statistics.median(a) if statistics.median(a) else float("nan")
    return f"Mann-Whitney U={res.statistic:.0f} p={res.pvalue:.4f} | mediana dopo/prima={ratio:.2f}"


METRICS_CALL = [
    ("sec", "agent call [s]"),
    ("out_chars", "output [char]"),
    ("chars_per_s", "output char/s"),
    ("prompt_chars", "prompt [char]"),
    ("tok_out", "tokens out"),
    ("tok_per_s", "tokens out/s"),
]
METRICS_REP = [
    ("elapsed", "rep elapsed [s]"),
    ("attempts", "attempts"),
    ("agent_s", "rep agent [s]"),
    ("judge_s", "rep judge [s]"),
]


def _print_series(label: str, data: Dict[str, List[Dict[str, Any]]]) -> None:
    print(f"  -- {label}")
    first = [c for c in data["calls"] if c["attempt"] == 1]
    for key, name in METRICS_CALL:
        print(f"     {name:<18} all   {_desc([c[key] for c in data['calls']])}")
        if key in ("sec", "chars_per_s", "out_chars"):
            print(f"     {name:<18} 1st   {_desc([c[key] for c in first])}")
    for key, name in METRICS_REP:
        print(f"     {name:<18} rep   {_desc([r[key] for r in data['reps']])}")
    nt = sum(c["native_thinking"] for c in data["calls"])
    print(f"     native_thinking presente in {nt}/{len(data['calls'])} chiamate")


def _by_run(data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    out: Dict[str, Dict[str, List]] = defaultdict(lambda: {"calls": [], "reps": []})
    for c in data["calls"]:
        out[c["run_id"]]["calls"].append(c)
    for r in data["reps"]:
        out[r["run_id"]]["reps"].append(r)
    return dict(sorted(out.items()))


def compare(task: str, before: str, after: str) -> None:
    pa, pb = _load(task, before), _load(task, after)
    print("=" * 100)
    print(f"{task}: {before}  ->  {after}")
    for exp, payloads in ((before, pa), (after, pb)):
        meta = {k: sorted({str(p.get(k)) for p in payloads}) for k in MODEL_META_KEYS if any(k in p for p in payloads)}
        extra = {k: sorted({str(p.get(k)) for p in payloads}) for k in ("prompt_variant", "is_hosted", "temperature")}
        print(f"  metadati {exp}: {meta} {extra}")
    da, db = _rows(pa), _rows(pb)
    for exp, d in ((before, da), (after, db)):
        _print_series(f"{exp} (tutte le run)", d)
        runs = _by_run(d)
        if len(runs) > 1:
            for rid, sub in runs.items():
                _print_series(f"{exp} run_id={rid}", sub)
    print("  -- test prima vs dopo")
    fa = [c for c in da["calls"] if c["attempt"] == 1]
    fb = [c for c in db["calls"] if c["attempt"] == 1]
    for key, name in (("sec", "agent call [s]"), ("chars_per_s", "output char/s"), ("out_chars", "output [char]")):
        print(f"     {name:<18} all   {_mw([c[key] for c in da['calls']], [c[key] for c in db['calls']])}")
        print(f"     {name:<18} 1st   {_mw([c[key] for c in fa], [c[key] for c in fb])}")
    print(f"     {'rep elapsed [s]':<18} rep   {_mw([r['elapsed'] for r in da['reps']], [r['elapsed'] for r in db['reps']])}")
    print(f"     {'attempts':<18} rep   {_mw([r['attempts'] for r in da['reps']], [r['attempts'] for r in db['reps']])}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", nargs="?")
    ap.add_argument("before", nargs="?")
    ap.add_argument("after", nargs="?")
    ap.add_argument("--all", action="store_true", help="run every pair in DEFAULT_PAIRS")
    args = ap.parse_args()
    if args.all:
        for t, b, a in DEFAULT_PAIRS:
            compare(t, b, a)
    elif args.task and args.before and args.after:
        compare(args.task, args.before, args.after)
    else:
        ap.error("give TASK BEFORE AFTER, or --all")


if __name__ == "__main__":
    main()
