"""SAST hint injection (2026-07-21 experiment): inject raw, unfiltered
SonarQube alerts into the agent prompt to measure their effect empirically,
against the no-SAST baseline in docs/sgv_protocol/10_dati_paper_no_sonarqube.md.

Data source: docs/sast_tools/ground_truth_vuln_files.json (converted once from
the team-provided ground_truth_vuln_files.xlsx — see docs/expert_review/01
§2 for why this dataset is ~93% code-style noise, 0/54 alerts matching a
target CVE).
"""

import json
from pathlib import Path
from typing import Dict, List

from agents.prompts import SAST_HINT_ALERT_LINE, SAST_HINT_FOOTER, SAST_HINT_HEADER

# task_id prefix -> nf_abbr in the alerts dataset
_TASK_NF_MAP = {
    "task5_vuln_pcf": "PCF",
    "task6_vuln_udr": "UDR",
    "task7_vuln_amf": "AMF",
    "task8_vuln_udm": "UDM",
}


def _task_nf(task_id: str) -> str:
    for prefix, nf in _TASK_NF_MAP.items():
        if task_id.startswith(prefix):
            return nf
    return ""


def _load_alerts(dataset_path: str) -> List[Dict]:
    path = Path(dataset_path)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("alerts", [])


def is_sast_hint_task(task_id: str) -> bool:
    """True when task_id maps to an NF with SAST alerts available."""
    return bool(_task_nf(task_id))


def build_sast_hint_block(task_id: str, dataset_path: str) -> str:
    """Assemble the unfiltered SAST hint block for this task's NF.

    Returns "" if the task has no mapped NF or the NF has no alerts."""
    nf = _task_nf(task_id)
    if not nf:
        return ""
    alerts = [a for a in _load_alerts(dataset_path) if a.get("nf_abbr") == nf]
    return build_sast_hint_block_from_alerts(alerts, tool="SonarQube")


def build_sast_hint_block_from_alerts(alerts: List[Dict], tool: str = "SonarQube") -> str:
    """Same hint block, from an already-selected list of alerts.

    Path-keyed entry point used by the generic mode (`--source-dir`), where
    there is no task_id to map to an NF: `utils/sast_ingest.py` decides *which*
    alerts belong to the file, this only renders them. Kept identical in format
    to the static path on purpose — a difference in the block would confound any
    comparison between the two modes.
    """
    if not alerts:
        return ""
    lines = [
        SAST_HINT_ALERT_LINE.format(
            line=a.get("line"),
            severity=a.get("severity"),
            rule_key=a.get("rule_key"),
            message=a.get("message"),
        )
        for a in sorted(alerts, key=lambda a: a.get("line") or 0)
    ]
    return SAST_HINT_HEADER.format(tool=tool) + "\n".join(lines) + SAST_HINT_FOOTER
