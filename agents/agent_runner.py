import json
import re
from typing import Any, Dict

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


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


def run_agent(
    task_content: str,
    system_prompt: str,
    model: str,
    temperature: float,
    base_url: str,
) -> Dict[str, Any]:
    llm = ChatOllama(model=model, temperature=temperature, base_url=base_url)
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=task_content)]
    response = llm.invoke(messages)
    return _extract_json_from_text(response.content)
