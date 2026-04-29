import json
import logging
import re
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
    return _extract_json_from_text(response.content)
