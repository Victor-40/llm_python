def build_point(id: int, text: str, embedding: list[float], source: str = "docs") -> dict:
    return {
        "id": id,
        "vector": embedding,
        "payload": {
            "text": text,
            "source": source
        }

    }