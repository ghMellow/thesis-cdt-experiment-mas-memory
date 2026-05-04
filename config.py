# Model mapping for each experiment role and judge.
MODELS = {
    "expert_1A": "gemma4:e2b",
    "beginner_1A": "gemma4:e2b",
    "expert_1B": "gemma4:e2b",
    "beginner_1B": "deepseek-r1:latest",
    "judge": "gemma4:e2b",
}

# Generation temperature (0.0 = deterministic).
TEMPERATURE = 0.0
# Max attempts per task before stopping.
MAX_RETRIES = 3
# Repetitions per task for consistency checks.
REPETITIONS = 3
# Max wall time per task repetition (seconds).
TASK_TIMEOUT_SECONDS = 600
# Pass threshold for textual tasks (ratio of rubric max score).
TEXTUAL_PASS_RATIO = 0.7

# Ollama server endpoint.
OLLAMA_BASE_URL = "http://localhost:11434"
# Limit generated tokens to reduce long responses.
OLLAMA_NUM_PREDICT = 256 #128, 256, 512
# Optional suffix to discourage long reasoning on specific tasks.
NO_THINK_SUFFIX = " /no_think"
# Max time to wait for a single Ollama response (seconds).
# Keep this >= TASK_TIMEOUT_SECONDS to avoid client timeouts before task timeouts.
# If --task-timeout is higher, runtime bumps this to ~10% above task_timeout.
OLLAMA_TIMEOUT_SECONDS = TASK_TIMEOUT_SECONDS * 1.1

# Input tasks and output results directories.
TASKS_PATH = "docs/tasks/"
RESULTS_PATH = "results/"
