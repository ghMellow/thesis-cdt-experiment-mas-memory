import json
import logging
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

import httpx
from langchain_core.messages import HumanMessage, SystemMessage

import config
from agents._llm_utils import (
    _expected_score_fields,
    _extract_judge_scores_markdown,
    _extract_json_from_text,
    _raise_ollama_unavailable,
    _start_spinner,
    build_llm,
)

logger = logging.getLogger(__name__)


def _strip_agent_instructions(task_content: str) -> str:
    marker = "\n## Agent Instructions"
    if marker in task_content:
        return task_content.split(marker, 1)[0].rstrip()
    return task_content.strip()


def _format_markdown_value(value: Any) -> str:
    if isinstance(value, dict):
        lines: List[str] = []
        for key, item in value.items():
            if isinstance(item, list):
                lines.append(f"{key}:")
                lines.extend([f"- {entry}" for entry in item])
            else:
                lines.append(f"{key}: {item}")
        return "\n".join(lines) if lines else ""
    if isinstance(value, list):
        return "\n".join([f"- {entry}" for entry in value])
    return str(value)


def _format_rubric_markdown(rubric: Dict[str, Any]) -> str:
    rubrica = rubric.get("rubrica", {})
    total_max = rubric.get("total_max")
    lines: List[str] = []
    if total_max is not None:
        lines.append(f"Total max score: {total_max}")
    for field, spec in rubrica.items():
        max_val = spec.get("max", 0)
        criteri = spec.get("criteri", {})
        lines.append(f"- {field} (0-{max_val})")
        for score, description in sorted(criteri.items(), key=lambda x: x[0], reverse=True):
            lines.append(f"  - {score}: {description}")
    return "\n".join(lines) if lines else "No rubric details provided."


def _format_agent_response_markdown(agent_response: Dict[str, Any]) -> str:
    return (
        "### Answer\n"
        f"{_format_markdown_value(agent_response.get('answer', ''))}\n\n"
        "### Reasoning\n"
        f"{agent_response.get('reasoning', '')}\n\n"
        "### Confidence\n"
        f"{agent_response.get('confidence', '')}"
    )


def _build_judge_payload_markdown(
    task_content: str,
    rubric: Dict[str, Any],
    agent_response: Dict[str, Any],
) -> str:
    scenario = _strip_agent_instructions(task_content)
    rubric_md = _format_rubric_markdown(rubric)
    response_md = _format_agent_response_markdown(agent_response)
    return (
        "## Scenario\n"
        f"{scenario}\n\n"
        "## Rubric\n"
        f"{rubric_md}\n\n"
        "## Agent Response\n"
        f"{response_md}\n"
    )


def run_judge_textual(
    task_content: str,
    rubric: Dict[str, Any],
    agent_response: Dict[str, Any],
    system_prompt: str,
    model: str,
    temperature: float,
    base_url: str,
    is_hosted: bool = False,
) -> Tuple[Dict[str, Any], Optional[int], Optional[int]]:
    llm = build_llm(model, temperature, base_url, is_hosted)
    payload = _build_judge_payload_markdown(task_content, rubric, agent_response)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=payload),
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
    expected_fields = _expected_score_fields(rubric)
    try:
        parsed = _extract_judge_scores_markdown(response.content, expected_fields)
    except ValueError:
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
    is_hosted: bool = False,
) -> Dict[str, Any]:
    """Check if multiple reasoning passages are semantically equivalent.

    Always uses temperature=0 for deterministic output.
    Returns {"equivalent": bool, "explanation": str}.
    On any error returns {"equivalent": False, "explanation": "<error msg>"}.
    """
    llm = build_llm(model, 0, base_url, is_hosted, num_predict=256)
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
