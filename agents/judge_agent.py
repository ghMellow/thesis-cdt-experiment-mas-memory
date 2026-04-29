import itertools
import json
import logging
import re
import sys
import threading
import time
from typing import Any, Dict

import httpx
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

import config

logger = logging.getLogger(__name__)


def _extract_json_from_text(text: str) -> Dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    code_block = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if code_block:
        return json.loads(code_block.group(1))

    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        return json.loads(brace_match.group(0))

    raise ValueError("No JSON object found in response")


def _start_spinner(label: str, stop_event: threading.Event) -> threading.Thread:
    def spin() -> None:
        for ch in itertools.cycle("|/-\\"):
            if stop_event.is_set():
                break
            sys.stderr.write(f"\r{label} {ch}")
            sys.stderr.flush()
            time.sleep(0.1)
        sys.stderr.write("\r" + " " * (len(label) + 2) + "\r")
        sys.stderr.flush()

    thread = threading.Thread(target=spin, daemon=True)
    thread.start()
    return thread


def _raise_ollama_unavailable(base_url: str) -> None:
    logger.error("Ollama endpoint not reachable at %s. Start it with `ollama serve`.", base_url)
    raise SystemExit(1)


def run_judge_textual(
    task_content: str,
    rubric: Dict[str, Any],
    agent_response: Dict[str, Any],
    system_prompt: str,
    model: str,
    temperature: float,
    base_url: str,
) -> Dict[str, Any]:
    llm = ChatOllama(
        model=model,
        temperature=temperature,
        base_url=base_url,
        timeout=config.OLLAMA_TIMEOUT_SECONDS,
        model_kwargs={"num_predict": config.OLLAMA_NUM_PREDICT},
    )
    payload = {
        "scenario": task_content,
        "rubrica": rubric,
        "agent_response": agent_response,
    }
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=json.dumps(payload, ensure_ascii=True)),
    ]
    sys.stderr.write("\n")
    sys.stderr.flush()
    logger.info("Judge active | model=%s | base_url=%s", model, base_url)
    stop_event = threading.Event()
    spinner = _start_spinner("Judge thinking", stop_event)
    start_perf = time.perf_counter()
    try:
        response = llm.invoke(messages)
    except httpx.ConnectError:
        _raise_ollama_unavailable(base_url)
    except httpx.ReadTimeout:
        logger.error(
            "Ollama request timed out after %ss. Increase OLLAMA_TIMEOUT_SECONDS if needed.",
            config.OLLAMA_TIMEOUT_SECONDS,
        )
        raise SystemExit(1)
    finally:
        stop_event.set()
        spinner.join()
    parsed = _extract_json_from_text(response.content)
    elapsed = time.perf_counter() - start_perf
    total_score = parsed.get("total_score") if isinstance(parsed, dict) else None
    if total_score is None:
        logger.info("Judge done | elapsed=%.2fs", elapsed)
    else:
        logger.info("Judge done | elapsed=%.2fs | total_score=%s", elapsed, total_score)
    return parsed
