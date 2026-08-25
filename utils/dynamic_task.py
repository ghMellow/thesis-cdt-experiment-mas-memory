"""Dynamic task construction: point at a directory, get one task per source file.

Generalization mode A (docs/generalizzazione/00_costruzione_dinamica_task.md):
instead of reading a hand-written `docs/tasks/<task>.md` paired with a
`_sol.md` holding ground truth + rubric, this module builds the prompt body in
memory from real source files. The wrapper text below is the genericized
version of `docs/tasks/task5_vuln_pcf.md` — everything is fixed except the code
block, which is the file under review.

What this mode gives up, explicitly (not silently):
- no ground truth, no CVE/CVSS deterministic matching (`utils/cvss_eval.py`
  is keyed on known task ids) — judgement is correctness-only, via the GT-free
  rubric v2 (`docs/judge_rubric/gtfree/rubric_v2_draft.json`);
- no completeness measure — that needs the external candidate enumerator
  (proposal G5/SAST) which was never built;
- cross-file vulnerabilities are invisible by construction (one file = one task).
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# Two review instructions, A/B-tested on 2026-08-25 over the 4 free5GC NF files
# (docs/generalizzazione/00_costruzione_dinamica_task.md). Measured, with the
# project's own spurious-match correction applied: same 9 TP either way, the
# exhaustive variant costing 6 extra FP (precision 14.3% -> 13.0%). It does make
# the model examine more of a large file (UDR: 4 -> 6 distinct functions flagged,
# and the `|.+` regex finding stabilizes from 1/3 to 3/3 repetitions), which is
# coverage — the one thing a GT-free run cannot measure. Hence: default off,
# switchable, neither variant lost.
REVIEW_INSTRUCTION_BASE = """Perform a **security code review** of the file below. \
Identify any security vulnerabilities, misconfigurations, or unsafe coding patterns \
present in the code."""

REVIEW_INSTRUCTION_EXHAUSTIVE = """Perform a **security code review** of the file below. \
Read it in full, function by function, before deciding what to report — do not select \
preventively or stop after finding the first few issues. Identify all security \
vulnerabilities, logic errors, misconfigurations and unsafe coding patterns present in \
the code; there is no limit on how many findings you may report, including minor ones or \
ones that recur with small variations across similar handlers."""


TASK_TEMPLATE = """# Security Code Review — {rel_path}

---

## Scenario

The following Go source file is part of a 5G core network function implementation.

{review_instruction}

```go
{code}
```

---

## Question

Identify all security vulnerabilities or misconfigurations present in this file. For each finding:

1. Name the vulnerability class (e.g., CORS misconfiguration, injection, information exposure, etc.)
2. Point to the specific lines or functions where the issue occurs
3. Explain the security impact in the context of a 5G core network
4. Propose a correct fix

If the file contains no security-relevant weakness, say so explicitly instead of \
reporting a finding you cannot ground in the code above.

---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Reasoning
Detailed analysis: vulnerability class, location, impact in 5G context, proposed fix

### Answer
Brief summary of the main vulnerability found (1-2 sentences)

### Confidence
0.0
```
"""


def _slug_from_path(rel_path: Path) -> str:
    """Slug of the file's path relative to the scanned root, used as task_id.

    Only purpose: stay compatible with the existing per-task result storage
    (`results/rawJson/<task_id>/...`). No other meaning attached to it.
    """
    return re.sub(r"[^a-zA-Z0-9]+", "_", str(rel_path)).strip("_").lower()


def estimate_tokens(text: str, chars_per_token: float) -> int:
    """Static pre-flight token estimate — a heuristic proxy, no LLM call.

    Deliberately a rough `len/chars_per_token`: the point is to decide *before*
    spending a call whether a file is statistically at risk, not to be exact.
    Note (docs/generalizzazione/...): staying under the threshold does NOT mean
    the model performs well on the file — long-context degradation was observed
    on task6_full with no context overflow at all.
    """
    return int(len(text) / chars_per_token)


def discover_source_files(
    source_dir: Path,
    extensions: List[str],
    exclude_patterns: List[str],
) -> List[Path]:
    files: List[Path] = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.suffix not in extensions:
            continue
        rel = str(path.relative_to(source_dir))
        if any(pattern in rel for pattern in exclude_patterns):
            continue
        files.append(path)
    return files


def load_gtfree_rubric(rubric_path: str) -> Dict[str, Any]:
    import json

    path = Path(rubric_path)
    if not path.exists():
        raise FileNotFoundError(
            f"GT-free rubric not found at {rubric_path} — dynamic mode has no "
            "per-task rubric to fall back on."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_dynamic_tasks(
    source_dir: str,
    rubric: Dict[str, Any],
    extensions: List[str],
    exclude_patterns: List[str],
    max_prompt_tokens: Optional[int],
    chars_per_token: float,
    exhaustive: bool = False,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """One task spec per source file under `source_dir`.

    Returns (specs, skipped): files whose estimated prompt size exceeds
    `max_prompt_tokens` are never sent to the model — they are logged AND
    returned, so the report can state the real denominator instead of quietly
    reporting on a subset. Pass None to disable the gate.
    """
    variant = "exhaustive" if exhaustive else "base"
    instruction = REVIEW_INSTRUCTION_EXHAUSTIVE if exhaustive else REVIEW_INSTRUCTION_BASE
    root = Path(source_dir)
    if not root.is_dir():
        raise NotADirectoryError(f"--source-dir is not a directory: {source_dir}")

    specs: List[Dict[str, Any]] = []
    skipped: List[str] = []
    for path in discover_source_files(root, extensions, exclude_patterns):
        rel = path.relative_to(root)
        try:
            code = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            logger.warning("Skip %s (not valid UTF-8)", rel)
            skipped.append(f"`{rel}` — not valid UTF-8")
            continue
        task_content = TASK_TEMPLATE.format(
            rel_path=rel, code=code, review_instruction=instruction
        )
        estimated = estimate_tokens(task_content, chars_per_token)
        if max_prompt_tokens and estimated > max_prompt_tokens:
            skipped.append(
                f"`{rel}` — pre-flight token gate (~{estimated:,} est. tok > "
                f"{max_prompt_tokens:,})"
            )
            continue
        specs.append(
            {
                "task_id": _slug_from_path(rel),
                # Kept for provenance in the saved result; never read back as a task file.
                "task_path": str(path),
                "sol_path": "",
                "task_type": "textual",
                "task_content": task_content,
                "rubric": rubric,
                "gtfree": True,
                # Which review instruction built this prompt — persisted with the
                # result so a report can never misattribute an A/B arm.
                "prompt_variant": variant,
                "estimated_tokens": estimated,
            }
        )

    if skipped:
        logger.warning(
            "Pre-flight token gate skipped %s file(s):\n  %s",
            len(skipped),
            "\n  ".join(skipped),
        )
    logger.info(
        "Dynamic tasks built from %s: %s file(s) | prompt variant: %s",
        source_dir, len(specs), variant,
    )
    return specs, skipped
