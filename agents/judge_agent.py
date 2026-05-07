import json
import logging
import sys
import threading
import time
from typing import Any, Dict

import httpx
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

import config
from agents._llm_utils import _extract_json_from_text, _raise_ollama_unavailable, _start_spinner

logger = logging.getLogger(__name__)


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
