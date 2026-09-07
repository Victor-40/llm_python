def prompt_to_chat_messages(prompt: str) -> list:
    if not isinstance(prompt, str):
        raise TypeError
    return [{"role": "user", "content": f"{prompt}"}]