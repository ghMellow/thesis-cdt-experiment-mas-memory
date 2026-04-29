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


def _start_spinner(stop_event: threading.Event) -> threading.Thread:
    def spin() -> None:
        for ch in itertools.cycle("|/-\\"):
            if stop_event.is_set():
                break
            sys.stderr.write(f"\rThinking {ch}")
            sys.stderr.flush()
            time.sleep(0.1)
        sys.stderr.write("\r" + " " * 20 + "\r")
        sys.stderr.flush()

    thread = threading.Thread(target=spin, daemon=True)
    thread.start()
    return thread


def _raise_ollama_unavailable(base_url: str) -> None:
    logger.error("Ollama endpoint not reachable at %s. Start it with `ollama serve`.", base_url)
    raise SystemExit(1)


def run_agent(
    task_content: str,
    system_prompt: str,
    model: str,
    temperature: float,
    base_url: str,
) -> Dict[str, Any]:
    user_content = task_content
    if config.NO_THINK_SUFFIX and "task2_math_real" in task_content:
        user_content = f"{task_content}{config.NO_THINK_SUFFIX}"
    llm = ChatOllama(
        model=model,
        temperature=temperature,
        base_url=base_url,
        timeout=config.OLLAMA_TIMEOUT_SECONDS,
        model_kwargs={"num_predict": config.OLLAMA_NUM_PREDICT},
    )
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_content)]
    stop_event = threading.Event()
    spinner = _start_spinner(stop_event)
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
        sys.stderr.write("\n")
        sys.stderr.flush()
    return _extract_json_from_text(response.content)
