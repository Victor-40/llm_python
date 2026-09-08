from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import VectorParams, Distance, PointStruct

# === 1. Данные ===
documents = [
    "FastAPI — это современный фреймворк для построения API на Python.",
    "Alembic используется для управления миграциями базы данных в SQLAlchemy.",
    "Docker упрощает развёртывание приложений через контейнеризацию."
]

# === 2. Embedding-модель ===
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 измерения
embeddings = model.encode(documents)

# === 3. Подключение к Qdrant ===
client = QdrantClient("localhost", port=6333)

# === 4. Удаление и создание коллекции ===
collection_name = "docs"
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# === 5. Загрузка данных ===
points = [
    PointStruct(
        id=i,
        vector=embedding.tolist(),
        payload={"text": doc, "source": "internal_docs"}
    )
    for i, (doc, embedding) in enumerate(zip(documents, embeddings))
]

client.upload_points(collection_name=collection_name, points=points)

# === 6. Поиск ===
query = "Как обновить структуру базы данных?"
query_vector = model.encode(query).tolist()

search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=1
)

# === 7. Вывод результата ===
print(search_results.points[0].payload["text"])