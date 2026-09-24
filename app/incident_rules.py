def is_incident(level: str) -> bool:
    return level in {"ERROR", "CRITICAL"}

def is_high_latency(response_time: int) -> bool:
    return response_time > 2000