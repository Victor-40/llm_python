from flashrank import Ranker, RerankRequest

# 1. Инициализируем reranker (модель загрузится автоматически)
ranker = Ranker()  # по умолчанию: "ms-marco-TinyBERT-L-2-v2"

# 2. Готовим данные: запрос + фрагменты от векторного поиска
query = "Как откатить миграцию в Alembic?"
passages = [
    {"id": 0, "text": "Alembic — инструмент для управления миграциями БД."},
    {"id": 1, "text": "Команда alembic downgrade позволяет откатить миграцию."},
    {"id": 2, "text": "Миграции применяются через alembic upgrade head."},
]

# 3. Запускаем reranking
request = RerankRequest(query=query, passages=passages)
results = ranker.rerank(request)

print(results)

# # Явное указание модели
# ranker = Ranker(model_name="ms-marco-MultiBERT-L-12")  # лучше для мультиязычных задач

# # Или загрузка кастомной модели (позже в курсе)
# ranker = Ranker(cache_dir="./my_models")


# from flashrank import Ranker, RerankRequest

# ranker = Ranker()
# MAX_TOKENS = 512  # лимит модели
# CHARS_PER_TOKEN = 4  # грубая оценка для русского

# def safe_rerank(query: str, passages: list[dict]) -> list:
#     """Reranking с защитой от переполнения контекста."""
#     # Обрезаем тексты до лимита (по символам, для простоты)
#     trimmed = [
#         {**p, "text": p["text"][:MAX_TOKENS * CHARS_PER_TOKEN]}
#         for p in passages
#     ]
#     request = RerankRequest(query=query, passages=trimmed)
#     return ranker.rerank(request)


# # 1. Сначала фильтруем по метаданным
# from qdrant_client.models import Filter, FieldCondition, MatchValue

# filter = Filter(
#     must=[
#         FieldCondition(key="source", match=MatchValue(value="internal_docs")),
#         FieldCondition(key="created_at", match=MatchValue(value="2025"))
#     ]
# )

# results = client.query_points(
#     collection_name="docs",
#     query_vector=query_vec,
#     query_filter=filter,
#     limit=20  # берём больше кандидатов для reranking
# )

# # 2. Извлекаем тексты для reranking
# passages = [
#     {"id": p.id, "text": p.payload["text"]}
#     for p in results.points
# ]

# # 3. Запускаем reranking только на отфильтрованных кандидатах
# reranked = ranker.rerank(RerankRequest(query=query, passages=passages))