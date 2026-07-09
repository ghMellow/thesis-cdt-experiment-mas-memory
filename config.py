import os

# Model mapping for each experiment role, judge, and semantic consistency checks.
# Each entry: local = model name for local Ollama, hosted = model name on ollama.com,
# use_hosted = True to route through the hosted API instead of localhost.
#
# Local models available: gemma4:e4b (9.6 GB), gemma4:e2b (7.2 GB),
#                         deepseek-r1:7b (4.7 GB), deepseek-r1:latest (5.2 GB)
#
# ── Framing experiment quick-reference (docs/experiments_framing.md) ──────────
# Change MODELS to match the desired setup before each run.
#
# Experiment  | expert_1A          | beginner_1A        | expert_1B           | beginner_1B        | use_hosted
# ----------- | ------------------ | ------------------ | ------------------- | ------------------ | ----------
# 1A baseline | gemma4:e4b (local) | gemma4:e4b (local) | —                   | —                  | False
# 1A hosted   | gemma3:12b-cloud   | gemma3:12b-cloud   | —                   | —                  | True
# B1 scaling  | gemma4:e2b (local) | —                  | —                   | —                  | False  (then repeat with e4b)
# B2 asym.    | —                  | —                  | gemma4:31b-cloud    | gemma4:e4b (local) | mixed (gemma3:4b/12b-cloud → 500 su ollama.com con payload tecnici)
# B3 inv.asym | gemma4:e4b (local) | gemma4:e2b (local) | —                   | —                  | False
#
# judge:          local=gemma4:e4b  hosted=nemotron-3-super:cloud  (medium usage)
# semantic_check: local=gemma4:e2b  hosted=gemma3:4b-cloud          (low usage)
# ─────────────────────────────────────────────────────────────────────────────
MODELS = {
    "expert_1A": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True  # framing_B1_cloud: hosted gemma4:31b-cloud (scaling up expert)
    },
    "beginner_1A": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True
    },
    "expert_1B": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True
    },
    "beginner_1B": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True  # gemma3:12b-cloud → 500 su ollama.com con payload tecnici
    },
    "judge": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True
    },
    "semantic_check": {
        "local": "gemma4:e2b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True  # framing_A1: use local to avoid hosted 500 errors
    },
}

# Ollama hosted API endpoint and credentials (set OLLAMA_API_KEY in your .env).
OLLAMA_HOSTED_BASE_URL = "https://ollama.com/v1"
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

# Generation temperature — use > 0 to measure real consistency across repetitions.
TEMPERATURE = 0.3
# Max attempts per task before stopping.
MAX_RETRIES = 3
# Repetitions per task for consistency checks.
REPETITIONS = 3
# Max wall time per task repetition (seconds).
TASK_TIMEOUT_SECONDS = 600
# Pass threshold for textual tasks (ratio of rubric max score).
TEXTUAL_PASS_RATIO = 0.7
# Tasks whose stem contains this substring get an extended timeout (multiplied by FULL_TASK_TIMEOUT_MULTIPLIER).
FULL_TASK_SUFFIX = "full"
# Multiplier applied to TASK_TIMEOUT_SECONDS for tasks matching FULL_TASK_SUFFIX.
FULL_TASK_TIMEOUT_MULTIPLIER = 2.0

# Ollama server endpoint.
OLLAMA_BASE_URL = "http://localhost:11434"
# Max tokens per response — 1024 is sufficient for a full JSON with reasoning.
OLLAMA_NUM_PREDICT = 1024
# Max time to wait for a single Ollama response (seconds).
# Keep this >= TASK_TIMEOUT_SECONDS to avoid client timeouts before task timeouts.
# If --task-timeout is higher, runtime bumps this to ~10% above task_timeout.
OLLAMA_TIMEOUT_SECONDS = TASK_TIMEOUT_SECONDS * 1.1

# Input tasks and output results directories.
TASKS_PATH = "docs/tasks/"
RESULTS_PATH = "results/"

# ── CVSS estimate (experiment 2b, Blocco B) ──────────────────────────────────
# On security-review tasks the agent also emits a structured CVSS 4.0 estimate,
# evaluated deterministically against the normalized CVE dataset (no LLM judge).
# Reported separately; never influences the correct/wrong verdict.
CVSS_ESTIMATE_ENABLED = True
CVSS_DATASET_PATH = "File_Free5gc_Vulnerabili/cve_metrics_normalized.json"
# Score proximity bands: (max |estimated - reference|, points). First match wins.
# Initial values from call 10 discussion — to be calibrated (doc §5.1).
CVSS_SCORE_BANDS = [(0.5, 3), (1.5, 2), (3.0, 1)]
