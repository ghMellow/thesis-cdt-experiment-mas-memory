"""CVSS estimate support for security-review tasks (experiment 2b, Blocco B).

Adds a structured CVSS 4.0 estimate to the classifier output on `vuln` tasks:
- prompt text lives in `agents/prompts.py` (single source for prompt content,
  see that file's docstring for the full assembly order)
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
from agents.prompts import CVSS_PROMPT_BLOCK, NF_CONTEXT_HINT


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
