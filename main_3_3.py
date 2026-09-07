import chromadb
from chromadb.utils import embedding_functions

# === 1. Данные ===
text = """
FastAPI — это современный веб-фреймворк для построения API на Python.
Он автоматически генерирует документацию и поддерживает асинхронность.

Alembic — это инструмент для управления миграциями базы данных в SQLAlchemy.
Он позволяет безопасно обновлять схему БД при изменении моделей.

Docker — это платформа для контейнеризации приложений.
Она упрощает развёртывание и изоляцию зависимостей.
"""

# === 2. Чанкинг ===
chunks = text.strip().split("\n\n")
print("📄 Разбили текст на чанки:", len(chunks))

# === 3. Embedding-функция ===
print("🧠 Настраиваем embedding-функцию...")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# === 4. Сохранение в Chroma ===
print("💾 Сохраняем в Chroma...")
client = chromadb.EphemeralClient()
collection = client.create_collection(name="docs", embedding_function=ef)
collection.add(
    ids=[f"doc_{i}" for i in range(len(chunks))],
    documents=chunks
)

# === 5. Поиск по запросу ===
query = "Как обновить структуру базы данных?"
print(f"\n🔍 Запрос: '{query}'")

results = collection.query(
    query_texts=[query],
    n_results=1
)

# === 6. Вывод результата ===
retrieved = results["documents"][0][0]
print("\n✅ Найден релевантный фрагмент:")
print(f"> {retrieved}")

print("\n➡️ Этот фрагмент можно передать в LLM как контекст для генерации ответа.")