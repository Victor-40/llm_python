from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

docs = [
    {"text": "FastAPI — фреймворк для API на языке Python.", "source": "docs"},
    {"text": "Ошибка 500 в логах.", "source": "logs"},
    {"text": "Alembic управляет миграциями базы данных в Python-проектах.", "source": "docs"}
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode([d["text"] for d in docs])

client = QdrantClient("localhost", port=6333)
if client.collection_exists("task2"):
    client.delete_collection("task2")

client.create_collection(
    collection_name="task2",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

points = [
    PointStruct(id=i, vector=emb.tolist(), payload=d)
    for i, (d, emb) in enumerate(zip(docs, embeddings))
]
client.upload_points("task2", points)

query = "Фреймворк на Python для API"
query_vec = model.encode(query).tolist()

result = client.query_points(
    "task2",
    query=query_vec,
    query_filter=Filter(must=[FieldCondition(key="source", match=MatchValue(value="docs"))]),
    limit=1
)
print(result.points[0].payload["text"])