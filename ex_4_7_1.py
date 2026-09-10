config = {"input_sanitized": True, "has_fallback": False}
flags = ["logging_enabled", "has_timeouts", "input_sanitized", "tools_safe", "has_fallback"]


result = all(map(lambda key: True if config.get(key) else False, flags))

