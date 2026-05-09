import json
import logging
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

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
) -> Tuple[Dict[str, Any], Optional[int], Optional[int]]:
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
    logger.info("Judge active | model=%s", model)
    stop_event = threading.Event()
    spinner = _start_spinner("Judge thinking", stop_event)
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
    parsed = _extract_json_from_text(response.content)
    elapsed = time.perf_counter() - t0
    meta = getattr(response, "response_metadata", {}) or {}
    in_tok = meta.get("prompt_eval_count")
    out_tok = meta.get("eval_count")
    total_score = parsed.get("total_score") if isinstance(parsed, dict) else None
    score_str = f" | total_score={total_score}" if total_score is not None else ""
    tok_str = f" | tokens in={in_tok} out={out_tok}" if in_tok is not None and out_tok is not None else ""
    logger.info("Judge done | elapsed=%.1fs%s%s", elapsed, score_str, tok_str)
    return parsed, in_tok, out_tok


def run_semantic_equivalence_check(
    task_id: str,
    reasonings: List[str],
    model: str,
    base_url: str,
) -> Dict[str, Any]:
    """Check if multiple reasoning passages are semantically equivalent.

    Always uses temperature=0 for deterministic output.
    Returns {"equivalent": bool, "explanation": str}.
    On any error returns {"equivalent": False, "explanation": "<error msg>"}.
    """
    llm = ChatOllama(
        model=model,
        temperature=0,
        base_url=base_url,
        timeout=config.OLLAMA_TIMEOUT_SECONDS,
        model_kwargs={"num_predict": 256},
    )
    system = (
        "You are a semantic equivalence checker. "
        "Given multiple reasoning passages about the same task, decide if they are "
        "semantically equivalent: same conclusion and same key claims, even if phrased differently. "
        'Respond ONLY with a JSON object: {"equivalent": true|false, "explanation": "one sentence"}.'
    )
    payload = {"task_id": task_id, "reasonings": reasonings}
    messages = [
        SystemMessage(content=system),
        HumanMessage(content=json.dumps(payload, ensure_ascii=True)),
    ]
    logger.debug("Semantic equivalence check | task=%s model=%s", task_id, model)
    try:
        response = llm.invoke(messages)
    except httpx.ConnectError:
        _raise_ollama_unavailable(base_url)
    except httpx.ReadTimeout:
        logger.error(
            "Ollama request timed out after %ss during semantic check.",
            config.OLLAMA_TIMEOUT_SECONDS,
        )
        raise SystemExit(1)
    parsed = _extract_json_from_text(response.content)
    if not isinstance(parsed, dict) or "equivalent" not in parsed:
        raise ValueError(f"Unexpected semantic check response for {task_id}: {response.content!r}")
    return parsed
