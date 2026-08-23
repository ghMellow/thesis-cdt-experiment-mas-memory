# Multi-Agent Experiment — 5G Scenarios

Controlled multi-agent experiment on 5G network scenarios using LangGraph and local LLMs via Ollama.
A single agent answers the tasks across two experimental setups (`1A` same model for agent and judge, `1B` different models).

The task set the agent is evaluated against is in [docs/tasks/](docs/tasks/).

---

## Quick start

```bash
poetry install
ollama serve
ollama pull gemma4:e2b
ollama pull gemma4:e4b
ollama pull deepseek-r1:latest

poetry run python main.py
```

## Key CLI flags

```bash
poetry run python main.py --experiment 1A --task task3_anomaly
poetry run python main.py --repetitions 1 --task-timeout 300
poetry run python main.py --export-graph graph.png
```
