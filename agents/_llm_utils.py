"""Shared LLM call utilities for agent and judge runners."""

import itertools
import json
import logging
import re
import sys
import threading
import time
from typing import Any, Dict

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
