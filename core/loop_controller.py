def should_retry(attempts: int, max_retries: int, verdict: str) -> bool:
    if verdict == "correct":
        return False
    return attempts < max_retries
