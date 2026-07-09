"""Shared LLM call utilities for agent and judge runners."""

import itertools
import json
import logging
import re
import sys
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def resolve_model_config(role_key: str) -> tuple:
    """Return (model_name, is_hosted) for a MODELS role key."""
    import config
    cfg = config.MODELS[role_key]
    is_hosted = cfg["use_hosted"]
    return (cfg["hosted"] if is_hosted else cfg["local"]), is_hosted


def build_llm(model: str, temperature: float, base_url: str, is_hosted: bool = False, num_predict: int = None):
    """Instantiate ChatOllama (local) or ChatOpenAI (ollama.com hosted) based on is_hosted."""
    import config
    tokens = num_predict if num_predict is not None else config.OLLAMA_NUM_PREDICT
    if is_hosted:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            base_url=config.OLLAMA_HOSTED_BASE_URL,
            api_key=config.OLLAMA_API_KEY,
            max_tokens=tokens,
        )
    from langchain_ollama import ChatOllama
    return ChatOllama(
        model=model,
        temperature=temperature,
        base_url=base_url,
        timeout=config.OLLAMA_TIMEOUT_SECONDS,
        model_kwargs={"num_predict": tokens},
    )


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


_MARKDOWN_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(?P<title>.+?)\s*$", re.MULTILINE)


def _normalize_heading(title: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
    return cleaned.split()[0] if cleaned else ""


def _extract_markdown_sections(text: str, expected: List[str]) -> Dict[str, str]:
    matches: List[Tuple[str, int, int]] = []
    for match in _MARKDOWN_HEADING_RE.finditer(text):
        key = _normalize_heading(match.group("title"))
        if key in expected:
            matches.append((key, match.start(), match.end()))

    if not matches:
        return {}

    sections: Dict[str, str] = {}
    for idx, (key, _start, end) in enumerate(matches):
        next_start = matches[idx + 1][1] if idx + 1 < len(matches) else len(text)
        content = text[end:next_start].strip()
        if content:
            sections[key] = content
    return sections


def _strip_fenced_block(text: str) -> str:
    content = text.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if len(lines) >= 2 and lines[-1].strip().startswith("```"):
            return "\n".join(lines[1:-1]).strip()
    return content


def _parse_numeric_strict(value: str) -> Optional[float]:
    raw = value.strip()
    if re.fullmatch(r"-?\d+(?:\.\d+)?(?:\s*[A-Za-z%]+)?", raw):
        match = re.search(r"-?\d+(?:\.\d+)?", raw)
        return float(match.group(0)) if match else None
    return None


def _parse_numeric_loose(value: str) -> Optional[float]:
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group(0)) if match else None


def _should_parse_kv_answer(lines: List[str]) -> bool:
    known_keys = {"mean", "std", "root_cause", "diagnostic_steps"}
    for line in lines:
        match = re.match(r"^([A-Za-z0-9_ -]+):", line)
        if not match:
            continue
        key = match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
        if key in known_keys:
            return True
    return False


def _parse_kv_answer_block(lines: List[str]) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    for line in lines:
        kv_match = re.match(r"^([A-Za-z0-9_ -]+):\s*(.*)$", line)
        if kv_match:
            key = kv_match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
            value = kv_match.group(2).strip()
            if value:
                numeric = _parse_numeric_strict(value)
                data[key] = numeric if numeric is not None else value
                current_key = None
            else:
                data[key] = []
                current_key = key
            continue

        item_match = re.match(r"^[-*]\s+(.*)$", line)
        if item_match and current_key and isinstance(data.get(current_key), list):
            data[current_key].append(item_match.group(1).strip())
            continue

        if current_key and isinstance(data.get(current_key), list):
            data[current_key].append(line)

    return data


def _extract_agent_response_markdown(text: str) -> Dict[str, Any]:
    # "cvss" matches the optional "### CVSS Estimate" section on vuln tasks;
    # listing it here also keeps its content out of the confidence section.
    sections = _extract_markdown_sections(text, ["answer", "reasoning", "confidence", "cvss"])
    if not sections:
        raise ValueError("Missing markdown sections")

    answer_raw = sections.get("answer")
    reasoning_raw = sections.get("reasoning")
    confidence_raw = sections.get("confidence")
    if not answer_raw or not reasoning_raw or not confidence_raw:
        raise ValueError("Missing required markdown sections")

    answer_block = _strip_fenced_block(answer_raw)
    answer_lines = [line.strip() for line in answer_block.splitlines() if line.strip()]
    if _should_parse_kv_answer(answer_lines):
        answer: Any = _parse_kv_answer_block(answer_lines)
    else:
        numeric = _parse_numeric_strict(answer_block)
        answer = numeric if numeric is not None else answer_block.strip()

    confidence_val = _parse_numeric_loose(confidence_raw)
    if confidence_val is None:
        raise ValueError("Confidence value not found")
    
    # Normalize confidence to [0, 1]
    # If > 1, assume percentage (0-100) or scale (0-10) and normalize
    if confidence_val > 1.0:
        if confidence_val > 100.0:
            confidence_val = confidence_val / 1000.0  # Very large number, assume per-mille or similar
        elif confidence_val > 10.0:
            confidence_val = confidence_val / 100.0   # Assume percentage
        else:
            confidence_val = confidence_val / 10.0    # Assume 0-10 scale
    
    # Clamp to [0, 1]
    confidence_val = max(0.0, min(1.0, confidence_val))

    result = {
        "answer": answer,
        "reasoning": _strip_fenced_block(reasoning_raw),
        "confidence": confidence_val,
    }
    cvss_raw = sections.get("cvss")
    if cvss_raw:
        from utils.cvss_utils import extract_cvss_estimate
        estimate = extract_cvss_estimate(cvss_raw)
        if estimate is not None:
            result["cvss_estimate"] = estimate
    return result


def _extract_judge_scores_markdown(text: str, expected_fields: List[str]) -> Dict[str, Any]:
    sections = _extract_markdown_sections(text, ["scores", "feedback"])
    scores_block = sections.get("scores")
    if not scores_block:
        raise ValueError("Scores section not found")

    scores: Dict[str, Any] = {}
    for line in scores_block.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        cleaned = cleaned.lstrip("-* ").strip()
        if ":" not in cleaned:
            continue
        key, value = cleaned.split(":", 1)
        key = key.strip()
        key_norm = key.lower().replace(" ", "_")
        if expected_fields and key_norm not in expected_fields and key not in expected_fields:
            continue
        key = key if key in expected_fields else key_norm
        numeric = _parse_numeric_loose(value)
        scores[key] = numeric if numeric is not None else value.strip()

    for field in expected_fields:
        if field == "total_score":
            continue
        scores.setdefault(field, 0)

    feedback = sections.get("feedback", "").strip()
    if feedback:
        scores["feedback"] = feedback
    return scores


def _expected_score_fields(rubric: Dict[str, Any]) -> List[str]:
    fields = list(rubric.get("rubrica", {}).keys())
    if "total_score" not in fields:
        fields.append("total_score")
    return fields


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
