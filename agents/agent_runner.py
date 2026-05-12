import logging
import threading
import time
from typing import Any, Dict, Optional, Tuple

import httpx
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

import config
from agents._llm_utils import (
    _extract_agent_response_markdown,
    _extract_json_from_text,
    _raise_ollama_unavailable,
    _start_spinner,
)

logger = logging.getLogger(__name__)


def run_agent(
    task_content: str,
    system_prompt: str,
    model: str,
    temperature: float,
    base_url: str,
) -> Tuple[Dict[str, Any], Optional[int], Optional[int]]:
    llm = ChatOllama(
        model=model,
        temperature=temperature,
        base_url=base_url,
        timeout=config.OLLAMA_TIMEOUT_SECONDS,
        model_kwargs={"num_predict": config.OLLAMA_NUM_PREDICT},
    )
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=task_content)]
    stop_event = threading.Event()
    spinner = _start_spinner("Agent thinking", stop_event)
    t0 = time.perf_counter()
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
    elapsed = time.perf_counter() - t0
    meta = getattr(response, "response_metadata", {}) or {}
    in_tok = meta.get("prompt_eval_count")
    out_tok = meta.get("eval_count")
    if in_tok is not None and out_tok is not None:
        logger.info("Agent response | elapsed=%.1fs | tokens in=%s out=%s", elapsed, in_tok, out_tok)
    else:
        logger.info("Agent response | elapsed=%.1fs", elapsed)
    try:
        parsed = _extract_agent_response_markdown(response.content)
    except ValueError:
        try:
            parsed = _extract_json_from_text(response.content)
        except ValueError:
            logger.warning(
                "Agent response | no valid Markdown or JSON | raw=%r",
                response.content[:300],
            )
            parsed = {
                "answer": "",
                "reasoning": "model produced no valid Markdown or JSON output",
                "confidence": 0.0,
            }
    return parsed, in_tok, out_tok
