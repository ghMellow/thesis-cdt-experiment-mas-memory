# Model mapping for each experiment role and judge.
MODELS = {
    "expert_1A": "qwen3.5:latest",
    "beginner_1A": "qwen3.5:latest",
    "expert_1B": "qwen3.5:latest",
    "beginner_1B": "deepseek-r1:latest",
    "judge": "qwen3.5:latest",
}

# Ollama server endpoint.
OLLAMA_BASE_URL = "http://localhost:11434"

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

# Input tasks and output results directories.
TASKS_PATH = "docs/tasks/"
RESULTS_PATH = "results/"
