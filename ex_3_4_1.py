from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

docs = [
    "FastAPI поддерживает автоматическую генерацию OpenAPI-документации.",
    "Alembic позволяет создавать и применять миграции базы данных.",
    "Docker упрощает развёртывание через контейнеризацию."
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs)

client = QdrantClient("localhost", port=6333)
if client.collection_exists("task1"):
    client.delete_collection("task1")

client.create_collection(
    collection_name="task1",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

points = [PointStruct(id=i, vector=emb.tolist(), payload={"text": d}) for i, (d, emb) in enumerate(zip(docs, embeddings))]
client.upload_points("task1", points)

query = "Как обновлять структуру БД?"
query_vec = model.encode(query).tolist()
result = client.query_points("task1", query=query_vec, limit=1)
print(result.points[0].payload["text"])