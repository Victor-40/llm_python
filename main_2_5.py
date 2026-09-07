# import ollama

# response = ollama.generate(
#     model='mistral',
#     prompt='Что такое Alembic?'
# )
# print(response['response'])

#######################################################

# import ollama

# for chunk in ollama.chat(
#     model='mistral',
#     messages=[{'role': 'user', 'content': 'Расскажи про миграции в БД'}],
#     stream=True
# ):
#     print(chunk['message']['content'], end='', flush=True)

##################################################################

import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": "Что такое Alembic?",
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 2048
        }
    }
)

print(response.json()["response"])