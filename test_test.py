import tiktoken

text = """
Alembic — это инструмент для управления миграциями базы данных в SQLAlchemy.
Он позволяет безопасно обновлять схему БД при изменении моделей.
"""

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
tokens = enc.encode(text)
print(len(tokens))