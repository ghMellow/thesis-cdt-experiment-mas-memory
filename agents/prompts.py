"""Single source for every prompt *text* (constants/templates) sent to an LLM.

The functions that assemble these pieces with runtime data (task content,
rubric, retry history) stay where they were, relative py. This file only holds the pieces that are pure
text, so it can be shared/read on its own without pulling in the rest of the
pipeline. Reading it top-to-bottom follows the assembly order below.

--- Agent call (main task-solving LLM) ---

final agent prompt =
  1. SYSTEM_PROMPTS[role]                         -> SystemMessage
  2. docs/tasks/<task>.md raw content              -> \
  3. + NF_CONTEXT_HINT   (if CVSS task, hint on)    | utils/cvss_utils.py:
  4. + CVSS_PROMPT_BLOCK (if CVSS task)            -> / inject_cvss_instructions()
  5. [+ retry addendum, built in utils/experiment_utils.py:build_retry_task_content,
        retries only]
  -> HumanMessage
  (assembled in utils/task_utils.py + utils/experiment_utils.py:_run_agent,
  sent in agents/agent_runner.py:run_agent)

--- Judge call (rubric-scoring LLM) ---

final judge prompt =
  1. utils/experiment_utils.py:build_judge_prompt(rubric)  -> SystemMessage
  2. task content (Agent Instructions stripped) + rubric + agent response,
     formatted in agents/judge_agent.py:_build_judge_payload_markdown
  -> HumanMessage

--- Semantic equivalence checker (separate minor LLM call) ---

SEMANTIC_CHECK_SYSTEM_PROMPT -> SystemMessage, used in
agents/judge_agent.py:run_semantic_equivalence_check
"""

SYSTEM_PROMPTS = {
    # Single agent framing (call 11: expert/beginner unified — 19/20 identical
    # verdicts across roles, the framing added no signal).
    "agent": """
You are a 5G network engineer experienced in core network analysis and code review.
Reply ONLY in Markdown using the response format in the task. No extra text before or after.
""",
}


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
#
# Split in header/footer + finding-line pieces so utils/cvss_utils.py can
# splice in the optional `snippet` line (SGV G3, config.SGV_SNIPPET_ENABLED)
# without duplicating the surrounding instructions.
CVSS_PROMPT_BLOCK_HEADER = """

---

## CVSS Estimate (required)

For each vulnerability reported in your Answer, also estimate its CVSS 4.0 base
metrics. Add this exact section to your response, after the Answer section and
before Confidence, repeating the {n} lines below for each finding. Each finding names exactly ONE
function: if the same vulnerability affects several functions, repeat the whole
block once per affected function (same vector/score, one `function:` line each)
instead of listing multiple function names in a single line.

### CVSS Estimate
"""

CVSS_PROMPT_FINDING_LINES_BASE = """\
- function: <name of the Go function containing the issue>
- vector: CVSS:4.0/AV:_/AC:_/AT:_/PR:_/UI:_/VC:_/VI:_/VA:_/SC:_/SI:_/SA:_
- score: <your estimated CVSS 4.0 base score, 0.0-10.0>"""

CVSS_PROMPT_FINDING_LINE_SNIPPET = (
    "- snippet: <one exact line of code, copied verbatim from the source above, "
    "that supports this finding>"
)

CVSS_PROMPT_BLOCK_FOOTER = """

Replace each `_` in the vector with one of the allowed values:

- AV Attack Vector: N (Network), A (Adjacent), L (Local), P (Physical)
- AC Attack Complexity: L (Low), H (High)
- AT Attack Requirements: N (None), P (Present)
- PR Privileges Required: N (None), L (Low), H (High)
- UI User Interaction: N (None), P (Passive), A (Active)
- VC / VI / VA Confidentiality / Integrity / Availability impact on the
  vulnerable system: H (High), L (Low), N (None)
- SC / SI / SA Confidentiality / Integrity / Availability impact on
  subsequent systems (other components reachable from the vulnerable one):
  H (High), L (Low), N (None)
"""

SEMANTIC_CHECK_SYSTEM_PROMPT = (
    "You are a semantic equivalence checker. "
    "Given multiple reasoning passages about the same task, decide if they are "
    "semantically equivalent: same conclusion and same key claims, even if phrased differently. "
    'Respond ONLY with a JSON object: {"equivalent": true|false, "explanation": "one sentence"}.'
)
