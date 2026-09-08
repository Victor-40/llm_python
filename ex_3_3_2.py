def chunk_text(text: str) -> list[str]:
    result = text.split("\n\n")
    return  [item.strip() for item in result if item.strip()]