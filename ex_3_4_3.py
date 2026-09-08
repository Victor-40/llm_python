from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

docs = [
    {"text": "Docker", "category": "infra", "version": "20.10"},
    {"text": "Alembic", "category": "db", "version": "1.13"},
    {"text": "FastAPI", "category": "api", "version": "0.100"}
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode([d["text"] for d in docs])

client = QdrantClient("localhost", port=6333)
if client.collection_exists("task3"):
    client.delete_collection("task3")

client.create_collection(
    collection_name="task3",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)


points = [
    PointStruct(id=i, vector=emb.tolist(), payload=d)
    for i, (d, emb) in enumerate(zip(docs, embeddings))
]
client.upload_points("task3", points)

query = "Инструмент для миграций"
query_vec = model.encode(query).tolist()
result = client.query_points("task3", query=query_vec, limit=1)
print(result.points[0].payload["category"])