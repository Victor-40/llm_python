from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("Как запустить миграцию?")

print(type(embedding))   # <class 'numpy.ndarray'>
print(embedding[:5])     # [-0.038, 0.031, -0.044, -0.042, 0.018, ...]
print(len(embedding))    # 384