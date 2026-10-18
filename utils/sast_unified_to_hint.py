"""Convert the team's unified multi-tool SAST report (format
`free5gc-sast-unificato` v3.0: gosec + Semgrep + CodeQL) into the alerts
dataset read by utils/sast_hint.py on the static task path.

    python -m utils.sast_unified_to_hint <unified.json> <out.json> [--check-reduced <ridotto.json>] [--with-linked-code]

Only alerts the agent can locate in its own file are kept: an alert whose line
is in the NF's ground-truth file, or whose taint source (`origine_dato`, CodeQL
only) is. The second kind is anchored to the source line, because the agent
never sees the destination file; the destination goes into the message instead.
With --with-linked-code the dataset also carries the report's own context lines
around each destination, which utils/sast_hint.py appends after the alerts.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# NF -> ground-truth file, relative to the NF folder as the unified report writes it.
GT_FILES = {
    "udr": "internal/sbi/api_datarepository.go",
    "udm": "internal/sbi/api_subscriberdatamanagement.go",
    "amf": "internal/sbi/api_communication.go",
    "pcf": "internal/sbi/api_oam.go",
}

_SEVERITY = {"critica": "CRITICAL", "alta": "HIGH", "media": "MEDIUM", "bassa": "LOW", "info": "INFO"}
_TOOL_NAME = {"codeql": "CodeQL", "gosec": "gosec", "semgrep": "Semgrep"}
# CodeQL messages reference flow steps as markdown links, e.g. "[user-provided value](1)".
_MD_LINK = re.compile(r"\[([^\]]+)\]\(\d+\)")

# The SonarQube dataset needed a warning that most alerts are code-style noise;
# saying that about these security-rule alerts would be false.
PROMPT_NOTE = ""


def _split_loc(loc: Optional[str]):
    if not loc:
        return None, None
    path, _, line = loc.rpartition(":")
    return path, int(line)


def select_gt_alerts(segnalazioni: List[Dict]) -> List[Dict]:
    """Alerts on the GT file, or whose taint source is on it."""
    selected = [
        s for s in segnalazioni
        if s["file"] == GT_FILES.get(s["nf"]) or _split_loc(s.get("origine_dato"))[0] == GT_FILES.get(s["nf"])
    ]
    # A tool without data-flow (gosec) reporting the same lines as an indirect
    # CodeQL alert has no source of its own: it inherits the twin's anchor.
    by_lines = {
        (s["nf"], s["file"], s["riga_inizio"]): s
        for s in segnalazioni
        if s.get("origine_dato") and _split_loc(s["origine_dato"])[0] == GT_FILES.get(s["nf"])
    }
    for s in segnalazioni:
        twin = by_lines.get((s["nf"], s["file"], s["riga_inizio"]))
        if twin and s is not twin and not s.get("origine_dato") and s not in selected:
            selected.append(s)
    return selected


def to_hint_alert(s: Dict, segnalazioni: List[Dict]) -> Dict:
    gt = GT_FILES[s["nf"]]
    tool = _TOOL_NAME.get(s["tool"], s["tool"])
    message = _MD_LINK.sub(r"\1", s["messaggio"]).rstrip(".")
    src_path, src_line = _split_loc(s.get("origine_dato"))

    if s["file"] == gt:
        line = s["riga_inizio"]
        if src_path == gt and src_line != line:
            message += f" (source at L{src_line})"
    else:
        if src_path != gt:
            twin = next(
                t for t in segnalazioni
                if t is not s and (t["nf"], t["file"], t["riga_inizio"]) == (s["nf"], s["file"], s["riga_inizio"])
                and _split_loc(t.get("origine_dato"))[0] == gt
            )
            src_line = _split_loc(twin["origine_dato"])[1]
        line = src_line
        message += (
            f". Reported in another file of this NF, {s['file']}:{s['riga_inizio']} "
            f"({s['funzione']}), reached by data flowing from this line"
        )

    rule = f"{tool} {s['regola']}" + (f" ({s['cwe']})" if s.get("cwe") else "")
    return {
        "nf_abbr": s["nf"].upper(),
        "line": line,
        "severity": _SEVERITY.get(s["gravita"], s["gravita"].upper()),
        "rule_key": rule,
        "message": message,
        "source_id": s["id"],
        "source_file": s["file"],
        "source_line": s["riga_inizio"],
    }


def linked_code(selected: List[Dict]) -> List[Dict]:
    """One snippet per destination outside the GT file, deduplicated: several
    alerts (two sources, or CodeQL plus its gosec twin) can share it."""
    seen = {}
    for s in selected:
        if s["file"] == GT_FILES[s["nf"]]:
            continue
        key = (s["nf"], s["file"], s["riga_inizio"])
        if key not in seen:
            seen[key] = {
                "nf_abbr": s["nf"].upper(),
                "file": s["file"],
                "line": s["riga_inizio"],
                "function": s["funzione"],
                "lines": s["contesto"],
            }
    return sorted(seen.values(), key=lambda c: (c["nf_abbr"], c["file"], c["line"]))


def convert(unified: Dict, with_linked_code: bool = False) -> Dict:
    seg = unified["segnalazioni"]
    selected = select_gt_alerts(seg)
    alerts = [to_hint_alert(s, seg) for s in selected]
    alerts.sort(key=lambda a: (a["nf_abbr"], a["line"], a["rule_key"]))
    extra = {"linked_code": linked_code(selected)} if with_linked_code else {}
    return {
        "_meta": {
            "source_format": f"{unified['formato']} v{unified['versione_formato']}",
            "scan_date": unified["metadati"].get("data_scansione"),
            "selection": "alert on the NF ground-truth file, or with origine_dato on it "
                         "(anchored to that line); gosec twin of an indirect CodeQL alert inherits its anchor",
            "count": len(alerts),
        },
        "tool": ", ".join(sorted({_TOOL_NAME.get(s["tool"], s["tool"]) for s in seg})),
        "prompt_note": PROMPT_NOTE,
        "alerts": alerts,
        **extra,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("unified")
    p.add_argument("out")
    p.add_argument("--check-reduced", help="team's reduced file: fail if the selection differs")
    p.add_argument("--with-linked-code", action="store_true",
                   help="also carry the context lines of each destination in another file")
    args = p.parse_args(argv)

    unified = json.loads(Path(args.unified).read_text(encoding="utf-8"))
    out = convert(unified, with_linked_code=args.with_linked_code)

    if args.check_reduced:
        reduced = json.loads(Path(args.check_reduced).read_text(encoding="utf-8"))
        want = {s["id"] for s in reduced["segnalazioni"]}
        got = {a["source_id"] for a in out["alerts"]}
        if want != got:
            print(f"selection differs from reduced file: missing {sorted(want - got)}, extra {sorted(got - want)}",
                  file=sys.stderr)
            return 1

    Path(args.out).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    per_nf: Dict[str, int] = {}
    for a in out["alerts"]:
        per_nf[a["nf_abbr"]] = per_nf.get(a["nf_abbr"], 0) + 1
    print(f"{len(out['alerts'])} alerts -> {args.out}  {per_nf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
