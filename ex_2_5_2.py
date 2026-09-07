def build_generate_request(model: str, prompt: str) -> dict:
    return {"model": f"{model}", "prompt": f"{prompt}"}

