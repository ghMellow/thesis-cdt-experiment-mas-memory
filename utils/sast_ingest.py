"""SAST report ingestion for generic mode: normalize, then join alerts to files.

Why the report is a frozen file and not a tool invocation
--------------------------------------------------------
The pipeline never runs the SAST tool. The tool version and its enabled ruleset
*are* part of the experimental condition: if the pipeline re-ran it, two runs a
month apart would silently stop being comparable. So the tool is run by hand,
its output frozen, and `--sast-report` points at that artifact — whose sha256
goes in the run report, making the run re-derivable.

Path joining
------------
The alert path and the reviewed file's path relative to `--source-dir` often do
not coincide: the tool usually reports repo-root-relative paths
(`NFs/amf/internal/sbi/api_communication.go`) while the scanned directory may be
a curated copy (`AMF/api_communication.go`). They are matched by longest common
path suffix, and **ambiguity is never guessed**: two different alert paths ending
in the same basename (`api_oam.go` is not rare in a Go repo) would otherwise
attach one file's alerts to another — a wrong result that still looks plausible,
the worst kind. Those files go to interactive resolution instead.
"""

import hashlib
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Normalized alert: {"path": str, "line": int|None, "severity": str,
#                    "rule_key": str, "message": str}
Alert = Dict[str, Any]


# Report format -> tool name as stated to the model in the prompt header. The
# project-normalized dataset is itself a SonarQube export, hence the label.
TOOL_LABEL = {
    "project-normalized": "SonarQube",
    "gosec": "gosec",
    "semgrep": "Semgrep",
}


class SastIngestError(RuntimeError):
    """Raised when the report cannot be read, parsed, or joined to any file."""


def _norm_project(data: Dict[str, Any]) -> List[Alert]:
    """docs/sast_tools/ground_truth_vuln_files.json (SonarQube export, annotated)."""
    out = []
    for a in data.get("alerts", []):
        # component_path is repo-root-relative, vuln_file is relative to the
        # curated vulnerable-files tree — keep the first, the suffix matcher
        # handles either shape.
        path = a.get("component_path") or a.get("vuln_file") or ""
        if not path:
            continue
        out.append({
            "path": path,
            "line": a.get("line"),
            "severity": a.get("severity") or "UNKNOWN",
            "rule_key": a.get("rule_key") or "",
            "message": a.get("message") or "",
        })
    return out


def _norm_gosec(data: Dict[str, Any]) -> List[Alert]:
    out = []
    for i in data.get("Issues", []):
        line = i.get("line")
        try:
            # gosec reports the line as a string, sometimes as a "12-14" range.
            line = int(str(line).split("-")[0])
        except (TypeError, ValueError):
            line = None
        out.append({
            "path": i.get("file") or "",
            "line": line,
            "severity": i.get("severity") or "UNKNOWN",
            "rule_key": i.get("rule_id") or "",
            "message": i.get("details") or "",
        })
    return [a for a in out if a["path"]]


def _norm_semgrep(data: Dict[str, Any]) -> List[Alert]:
    out = []
    for r in data.get("results", []):
        extra = r.get("extra") or {}
        out.append({
            "path": r.get("path") or "",
            "line": (r.get("start") or {}).get("line"),
            "severity": extra.get("severity") or "UNKNOWN",
            "rule_key": r.get("check_id") or "",
            "message": extra.get("message") or "",
        })
    return [a for a in out if a["path"]]


def load_alerts(report_path: str) -> Tuple[List[Alert], str, str]:
    """Read a SAST report, auto-detecting the format.

    Returns (alerts, format_name, sha256) — the digest goes in the run report so
    the exact artifact behind a run is identifiable later.
    """
    path = Path(report_path)
    if not path.is_file():
        raise SastIngestError(f"--sast-report not found: {report_path}")
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()[:16]
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SastIngestError(f"--sast-report is not valid JSON: {report_path} ({exc})") from exc
    if not isinstance(data, dict):
        raise SastIngestError(f"--sast-report must be a JSON object: {report_path}")

    if "alerts" in data:
        alerts, fmt = _norm_project(data), "project-normalized"
    elif "Issues" in data:
        alerts, fmt = _norm_gosec(data), "gosec"
    elif "results" in data:
        alerts, fmt = _norm_semgrep(data), "semgrep"
    else:
        raise SastIngestError(
            f"Unrecognized SAST report format in {report_path} — expected a top-level "
            "'alerts' (project-normalized), 'Issues' (gosec) or 'results' (semgrep) key"
        )
    if not alerts:
        raise SastIngestError(f"{report_path} parsed as {fmt} but contains zero alerts")
    logger.info("SAST report: %s alert(s) from %s (%s, sha256:%s)",
                len(alerts), report_path, fmt, digest)
    return alerts, fmt, digest


def _suffix_score(a: Path, b: Path) -> int:
    """Number of trailing path segments two paths have in common (0 = unrelated)."""
    score = 0
    for x, y in zip(reversed(a.parts), reversed(b.parts)):
        if x != y:
            break
        score += 1
    return score


def match_alerts(
    alerts: List[Alert], rel_paths: List[str]
) -> Tuple[Dict[str, List[Alert]], List[Tuple[str, List[str]]], List[str]]:
    """Join alerts to reviewed files by longest common path suffix.

    Returns (matched, ambiguous, absent) — three outcomes, not two, because
    "no alerts" and "could not tell which alerts" are different facts and
    conflating them is what makes a SAST arm quietly wrong:

    - `matched`: rel_path -> alerts, exactly one best-scoring alert path;
    - `ambiguous`: (rel_path, tied candidates) — two or more alert paths share
      the best score (e.g. `api_oam.go` living in two packages). Never guessed:
      attaching another file's alerts produces a wrong result that still looks
      plausible. Resolved by asking.
    - `absent`: not even the basename appears anywhere in the report. A SAST
      report only lists files that *have* findings, so this is the ordinary case
      for most of a real tree — reported in aggregate, not file by file, since
      prompting per file would be unusable on a repo of any size.
    """
    by_alert_path: Dict[str, List[Alert]] = {}
    for a in alerts:
        by_alert_path.setdefault(a["path"], []).append(a)
    alert_paths = list(by_alert_path)

    matched: Dict[str, List[Alert]] = {}
    ambiguous: List[Tuple[str, List[str]]] = []
    absent: List[str] = []
    for rel in rel_paths:
        rel_p = Path(rel)
        scored = [(p, _suffix_score(rel_p, Path(p))) for p in alert_paths]
        best = max((s for _, s in scored), default=0)
        if best == 0:
            absent.append(rel)
            continue
        winners = [p for p, s in scored if s == best]
        if len(winners) > 1:
            logger.warning(
                "SAST path ambiguity for `%s`: %s alert paths tie at %s common segment(s)",
                rel, len(winners), best,
            )
            ambiguous.append((rel, winners))
            continue
        matched[rel] = by_alert_path[winners[0]]
    return matched, ambiguous, absent


def confirm_absent(absent: List[str], alert_paths_total: int) -> List[Tuple[str, List[str]]]:
    """Ask once whether the files the report never mentions really have no alerts.

    One aggregate question rather than one per file: on a real tree this group is
    most of it. Answering "no" drops the whole group into per-file resolution, so
    a genuine path-convention mismatch is still recoverable by hand. Outside a
    terminal the group is accepted with a loud log — otherwise a reproducible
    re-run of an already-resolved pairing could never be scripted.
    """
    if not absent:
        return []
    logger.warning(
        "%s reviewed file(s) appear nowhere in the SAST report (not even by "
        "filename) — for these the 'with SAST' arm runs as the baseline: %s",
        len(absent), ", ".join(f"`{r}`" for r in absent[:10])
        + (f" (+{len(absent) - 10} more)" if len(absent) > 10 else ""),
    )
    if not sys.stdin.isatty():
        logger.warning("Not a terminal: treating all of them as 'no alerts'.")
        return []
    print(
        f"\n{len(absent)} of the reviewed files match no path in the SAST report "
        f"(the report covers {alert_paths_total} file path(s)).\n"
        "That is normal — a SAST report only lists files that have findings.",
        file=sys.stderr,
    )
    answer = input("Treat all of them as 'no alerts'? [Y/n]: ").strip().lower()
    if answer in ("", "y", "yes"):
        return []
    return [(rel, []) for rel in absent]


def _rank_candidates(rel_p: Path, alert_paths: List[str], limit: int = 10) -> List[str]:
    """Alert paths most plausibly corresponding to `rel_p`, best first."""
    ranked = sorted(
        alert_paths,
        key=lambda p: (_suffix_score(rel_p, Path(p)), Path(p).stem == rel_p.stem),
        reverse=True,
    )
    return ranked[:limit]


def resolve_interactively(
    unresolved: List[Tuple[str, List[str]]],
    alerts: List[Alert],
) -> Dict[str, Optional[str]]:
    """Ask the user, file by file, which alert path corresponds to it.

    Deliberately interactive rather than a log line: an unmatched file means the
    "with SAST" arm silently degrades to the baseline for that file, which would
    corrupt the comparison without any visible sign. The answer is returned as a
    mapping so it can be persisted (`--sast-path-map`) and the next run of the
    same pair repeats it without prompting.

    A value of None means "this file genuinely has no alerts" — a legitimate,
    explicit answer, distinct from "not asked".
    """
    if not sys.stdin.isatty():
        listing = "\n  ".join(rel for rel, _ in unresolved)
        raise SastIngestError(
            f"{len(unresolved)} reviewed file(s) have an ambiguous SAST match and "
            f"stdin is not interactive:\n  {listing}\n"
            "Re-run in a terminal to resolve them, or pass --sast-path-map with a JSON "
            'object {"<path relative to --source-dir>": "<path in the SAST report>" | null}.'
        )

    by_alert_path: Dict[str, List[Alert]] = {}
    for a in alerts:
        by_alert_path.setdefault(a["path"], []).append(a)

    mapping: Dict[str, Optional[str]] = {}
    print(
        f"\n=== SAST path resolution — {len(unresolved)} file(s) needing a decision ===\n"
        "For each file: pick a number, paste the path as it appears in the SAST "
        "report, or press ENTER for \"no alerts for this file\".\n",
        file=sys.stderr,
    )
    for rel, candidates in unresolved:
        print(f"File under review: {rel}", file=sys.stderr)
        if candidates:
            for idx, cand in enumerate(candidates, 1):
                n = len(by_alert_path.get(cand, []))
                print(f"  [{idx}] {cand}  ({n} alert(s))", file=sys.stderr)
        else:
            print("  (no candidate path in the report — paste one if you know it)",
                  file=sys.stderr)
        while True:
            answer = input("  path or number [ENTER = none]: ").strip()
            if not answer:
                mapping[rel] = None
                print("  -> no alerts recorded for this file\n", file=sys.stderr)
                break
            if answer.isdigit() and 1 <= int(answer) <= len(candidates):
                chosen = candidates[int(answer) - 1]
            elif answer in by_alert_path:
                chosen = answer
            else:
                print(f"  '{answer}' is not a path present in the report — retry.",
                      file=sys.stderr)
                continue
            mapping[rel] = chosen
            print(f"  -> {chosen} ({len(by_alert_path[chosen])} alert(s))\n", file=sys.stderr)
            break
    return mapping


def apply_path_map(
    path_map: Dict[str, Optional[str]], alerts: List[Alert]
) -> Dict[str, List[Alert]]:
    """Turn a rel_path -> alert_path mapping into rel_path -> alerts."""
    by_alert_path: Dict[str, List[Alert]] = {}
    for a in alerts:
        by_alert_path.setdefault(a["path"], []).append(a)
    out: Dict[str, List[Alert]] = {}
    for rel, alert_path in path_map.items():
        if alert_path is None:
            continue
        if alert_path not in by_alert_path:
            raise SastIngestError(
                f"path map points `{rel}` at `{alert_path}`, which is not in the "
                "SAST report — stale map, or wrong report file"
            )
        out[rel] = by_alert_path[alert_path]
    return out


def load_path_map(path: str) -> Dict[str, Optional[str]]:
    p = Path(path)
    if not p.is_file():
        raise SastIngestError(f"--sast-path-map not found: {path}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SastIngestError(f"--sast-path-map must be a JSON object: {path}")
    return data


def save_path_map(path: str, mapping: Dict[str, Optional[str]]) -> None:
    Path(path).write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    logger.info("SAST path map saved to %s (%s entries) — next run won't prompt",
                path, len(mapping))
