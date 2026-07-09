"""CVSS estimate support for security-review tasks (experiment 2b, Blocco B).

Adds a structured CVSS 4.0 estimate to the classifier output on `vuln` tasks:
- `CVSS_PROMPT_BLOCK` is appended to the task content at load time
- `extract_cvss_estimate` parses the agent's `### CVSS Estimate` markdown
  section into the internal dict shape ({"findings": [...]})

Project convention: LLM I/O is Markdown, code-side data is JSON — the agent
writes key/value markdown lines, this module converts them to the structure
used by `utils/cvss_eval.py` (deterministic evaluation, no LLM judge).
The rubric-based judge evaluation (Blocco A) is untouched.
"""

import json
import re
from typing import Any, Dict, List, Optional

import config

# NF context hint (team discussion 2026-07-09, proposal by Lorenzo Cannella):
# a human reviewer scores impact knowing the role of the NF inside the wider
# system; the excerpt alone doesn't say it's free5GC or that SBI traffic runs
# behind OAuth2/TLS by default. This is the minimal-cost variant, tested
# before the more expensive option (passing the whole free5GC repo as context).
NF_CONTEXT_HINT = """

**System context:** the code under review is a Network Function (NF) inside \
a 5G core network (free5GC architecture). In a standard 5G core deployment, \
the Service-Based Interface (SBI) between NFs runs behind mutual TLS and \
OAuth2 authorization by default. Use this when judging the *impact* \
(confidentiality/integrity/availability) of a vulnerability: do not assume a \
bug automatically exposes data — consider what is actually reachable or \
corrupted given this baseline.
"""

# Legend gives the full value space per metric (never the ground-truth values).
# Kept in sync with `_meta.legenda_metriche` in the normalized CVE dataset.
CVSS_PROMPT_BLOCK = """

---

## CVSS Estimate (required)

For each vulnerability reported in your Answer, also estimate its CVSS 4.0 base
metrics. Add this exact section to your response, between Reasoning and Confidence,
repeating the three lines below for each finding:

### CVSS Estimate
- function: <name of the Go function containing the issue>
- vector: CVSS:4.0/AV:_/AC:_/AT:_/PR:_/UI:_/VC:_/VI:_/VA:_
- score: <your estimated CVSS 4.0 base score, 0.0-10.0>

Replace each `_` in the vector with one of the allowed values:

- AV Attack Vector: N (Network), A (Adjacent), L (Local), P (Physical)
- AC Attack Complexity: L (Low), H (High)
- AT Attack Requirements: N (None), P (Present)
- PR Privileges Required: N (None), L (Low), H (High)
- UI User Interaction: N (None), P (Passive), A (Active)
- VC / VI / VA Confidentiality / Integrity / Availability impact on the
  vulnerable system: H (High), L (Low), N (None)
"""


def is_cvss_task(task_id: str, task_type: str) -> bool:
    """Security-review textual tasks are the only ones with a CVSS estimate."""
    return task_type == "textual" and "vuln" in task_id


def inject_cvss_instructions(task_content: str) -> str:
    hint = NF_CONTEXT_HINT if getattr(config, "CVSS_CONTEXT_HINT_ENABLED", False) else ""
    return task_content + hint + CVSS_PROMPT_BLOCK


_KV_LINE_RE = re.compile(r"^[-*\s]*(function|vector|score)\s*:\s*(.+)$", re.IGNORECASE)


def _parse_markdown_findings(text: str) -> List[Dict[str, Any]]:
    """Parse repeated `function:` / `vector:` / `score:` markdown lines into
    finding dicts. A new `function:` line starts a new finding."""
    findings: List[Dict[str, Any]] = []
    current: Dict[str, Any] = {}
    for line in text.splitlines():
        match = _KV_LINE_RE.match(line.strip())
        if not match:
            continue
        key = match.group(1).lower()
        value = match.group(2).strip().strip("`*")
        if key == "function":
            if current:
                findings.append(current)
            current = {"function": value}
        elif key == "score":
            num = re.search(r"-?\d+(?:\.\d+)?", value)
            current["score"] = float(num.group(0)) if num else value
        else:
            current[key] = value
    if current:
        findings.append(current)
    return [f for f in findings if "function" in f or "vector" in f or "score" in f]


def extract_cvss_estimate(section_text: str) -> Optional[Dict[str, Any]]:
    """Parse the `### CVSS Estimate` section content into {"findings": [...]}.

    Primary format is markdown key/value lines (project convention: MD toward
    the LLM, JSON on the code side). A fenced/inline JSON object is accepted
    as fallback for models that answer in JSON anyway. When nothing parses,
    returns {"_raw": <text>} so the raw output is preserved for inspection.
    Returns None on empty input.
    """
    if not section_text or not section_text.strip():
        return None
    text = section_text.strip()

    findings = _parse_markdown_findings(text)
    if findings:
        return {"findings": findings}

    code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = code_block.group(1) if code_block else None
    if candidate is None:
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        candidate = brace_match.group(0) if brace_match else None

    if candidate is not None:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    return {"_raw": text}
