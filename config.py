MODELS = {
    "expert_1A": "qwen3:9b",
    "beginner_1A": "qwen3:9b",
    "expert_1B": "qwen3:9b",
    "beginner_1B": "deepseek-r1:7b",
    "judge": "qwen3:9b",
}

OLLAMA_BASE_URL = "http://localhost:11434"

TEMPERATURE = 0.0
MAX_RETRIES = 3
REPETITIONS = 3
TEXTUAL_PASS_RATIO = 0.7

TASKS_PATH = "docs/tasks/"
RESULTS_PATH = "results/"
