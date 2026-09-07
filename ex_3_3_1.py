from chromadb.utils import embedding_functions
import chromadb

documents = [
    "FastAPI — это современный фреймворк для построения API на Python.",
    "Alembic используется для управления миграциями базы данных в SQLAlchemy.",
    "Docker упрощает развёртывание приложений через контейнеризацию."
]

query = "Как обновить структуру базы данных?"

# Настройка Chroma
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.Client()
collection = client.create_collection(name="docs", embedding_function=ef)

# Добавление документов
collection.add(
    ids=[f"id_{i}" for i in range(len(documents))],
    documents=documents
)

# Поиск
results = collection.query(query_texts=[query], n_results=1)

# Вывод ТОЛЬКО текста (без лишних слов)
print(results["documents"][0][0])