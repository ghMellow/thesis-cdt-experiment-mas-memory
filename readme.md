# User Guide - Multi-Agent Experiment

**Version:** 1.0
**Date:** 2026-04-29

This project runs controlled multi-agent experiments on a fixed set of tasks. It compares expert vs beginner roles across two experiment setups, logs answers and judgments, and writes results and evaluation reports for later analysis.

This guide explains how to run experiments without reading the code. It covers setup with Poetry or a Python virtual environment, CLI commands, logs, and how to stop/resume safely.

## Contents

- **<u>[Experiment setups (1A vs 1B)](#experiment-setups-1a-vs-1b)</u>**
- **<u>[Roles and tasks](#roles-and-tasks)</u>**
- [Outputs](#outputs)
- [Quick start (Poetry)](#quick-start-poetry)
- [Alternative setup (venv + requirements.txt)](#alternative-setup-venv--requirementstxt)
- [Ollama prerequisites](#ollama-prerequisites)
- **<u>[CLI commands](#cli-commands)</u>**
- [Logs and live progress](#logs-and-live-progress)
- [Stop, resume, and skip completed work](#stop-resume-and-skip-completed-work)
- **<u>[Troubleshooting](#troubleshooting)</u>**

## Experiment setups (1A vs 1B)

- **1A**: expert and beginner use the same model (control condition).
- **1B**: expert and beginner use different models (comparison condition).

The task set is the same for both setups so you can compare outcomes across conditions.

These labels are experiment codes. If you add new configurations, follow the same pattern (e.g., 1C, 2A) and refer to them by code in the CLI.

## Roles and tasks

Roles:
- **expert**: senior 5G engineer profile (more experienced).
- **beginner**: junior 5G technician profile (less experienced).

Tasks (in `docs/tasks/`):
- **task1_math_int**: integer math check (Python function compares against ground truth).
- **task2_math_real**: real-valued math check with tolerance (Python function compares against ground truth).
- **task3_anomaly**: anomaly detection / classification task (scored by judge LLM).
- **task4_rootcause**: root-cause analysis task (scored by judge LLM).

---

## Outputs

Json results are stored under:

```
results/
  1A/
    expert/
    beginner/
  1B/
    expert/
    beginner/
  evaluation/
```

The `evaluation/` folder contains Markdown summaries (`scores_*.md`, `comparison.md`). Task outputs are stored as JSON in the experiment/role folders.

Each task repetition writes two files:
- `<task_id>_repN.json` (the full result)
- `<task_id>_repN_solution.json` (ground truth snapshot)

The result JSON includes:
- `started_at`, `finished_at`, `elapsed_seconds`
- `attempts`, `verdict`, `final_answer`, and history

---

## Quick start (Poetry)

```bash
poetry install
poetry run python main.py --experiment 1A
```

If you need the shell:

```bash
poetry shell
python main.py --experiment 1A
```

---

## Alternative setup (venv + requirements.txt)

If you want a plain venv instead of Poetry, you need a requirements.txt. You can export it from Poetry:

```bash
poetry export -f requirements.txt --output requirements.txt
```

Then create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --experiment 1A
```

---

## Ollama prerequisites

The app uses Ollama locally. Make sure the server is running and models are pulled:

```bash
ollama serve
ollama pull qwen3:9b
ollama pull deepseek-r1:7b
```

If you see a 404 like `model 'qwen3:9b' not found`, run `ollama list` and pull the missing model.

---

## CLI commands

Examples:

```bash
# All experiments and roles
poetry run python main.py

# One experiment, one role, one task
poetry run python main.py --experiment 1A --role expert --task task1_math_int

# Custom timeout and repetitions
poetry run python main.py --task-timeout 600 --repetitions 1
```

Flags:
- `--experiment {1A|1B|all}`
- `--role {expert|beginner|all}`
- `--task <task_id>` (repeatable)
- `--repetitions <int>`
- `--task-timeout <seconds>`

Notes:
- **Required arguments:** none. Running `python main.py` executes everything.
- **Defaults:** `--experiment all`, `--role all`, and all tasks in `docs/tasks/`.
- **Reduction behavior:** adding any of `--experiment`, `--role`, or `--task` narrows what will run in that launch.
- Task IDs are the file stems (e.g., `task1_math_int`).

---

## Logs and live progress

During execution you will see:
- An info line when an experiment/role starts.
- The current task ID being processed.
- The repetition number.
- A minimal spinner with the text `Thinking` while the model is responding.
- A completion line with verdict and attempt count.
- A timeout warning and exit message if a task exceeds the time limit.
- A final line when evaluation reports are written.

This is designed to be minimal and not spam the console.

---

## Stop, resume, and skip completed work

You can stop the run at any time with Ctrl+C. When you re-run:
- The code checks `results/<experiment>/<role>/` and skips any task/repetition that already has a JSON file.
- Missing repetitions are automatically resumed.

Example:
- You set repetitions to 3.
- If `task1_math_int_rep1.json` and `task1_math_int_rep2.json` exist but rep3 does not, only rep3 will run.
- If all reps exist for a task, the runner skips that task and moves on.

This makes it safe to interrupt and resume without losing progress.

Timeout behavior:
- Each task repetition has a max wall time (default 600s).
- If a timeout happens, the program exits with an error so you can restart Ollama if needed.
- On the next run, completed repetitions are skipped automatically.

---

## Troubleshooting

- **Model not found (404):** Pull the model with `ollama pull <model>`.
- **Endpoint not reachable:** Run `ollama serve` to start the local server.
- **Very slow runs:** Start with `--repetitions 1` or a single task.
- **No progress visible:** You should still see the `Thinking` spinner. If not, check Ollama server status.
