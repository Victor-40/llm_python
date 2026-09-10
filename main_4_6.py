from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage


# === Состояние ===
class State(TypedDict):
    messages: Annotated[list, add_messages]
    task_id: str


# === Инструменты ===
@tool
def create_task() -> str:
    """Создаёт задачу и возвращает её ID."""
    return "TASK-123"


@tool
def add_comment(task_id: str, comment: str) -> str:
    """Добавляет комментарий к задаче по ID."""
    return f'Комментарий "{comment}" успешно добавлен к задаче с ID {task_id}.'


tools = [create_task, add_comment]
tool_node = ToolNode(tools)


# === LLM ===
llm = ChatOllama(model="qwen3.5:4b", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# === Узел агента ===
def call_model(state: State):
    system = SystemMessage(
        content=f"Ты — агент управления задачами. Текущий task_id: {state['task_id'] or 'не задан'}. "
                "Если задача не создана — сначала вызови create_task. Не выдумывай ID."
    )
    messages = [system] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}


# === Узел обновления состояния ===
def update_task_id(state: State):
    for msg in reversed(state["messages"]):
        if isinstance(msg, ToolMessage) and msg.name == "create_task":
            return {"task_id": msg.content}
    return {"task_id": state["task_id"]}


# === Сборка графа ===
workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_node("update", update_task_id)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    lambda state: "tools" if state["messages"][-1].tool_calls else "__end__"
)
workflow.add_edge("tools", "update")
workflow.add_edge("update", "agent")

app = workflow.compile()

# === Запуск с пошаговым выводом ===
if __name__ == "__main__":
    state = {"messages": [], "task_id": ""}

    # Шаг 1: создание задачи
    print("---- Шаг 1: Создание задачи ----")
    state = app.invoke({
        **state,
        "messages": [HumanMessage(content="Создай задачу: проверка подписки")]
    })
    print(f"Состояние после шага 1: task_id = '{state['task_id']}'")

    # Шаг 2: добавление комментария
    print("\n---- Шаг 2: Добавление комментария ----")
    state = app.invoke({
        **state,
        "messages": [HumanMessage(content="Добавь комментарий: протестировано")]
    })
    print(f"Состояние после шага 2: task_id = '{state['task_id']}'")

    # Финальный ответ
    last_msg = state["messages"][-1]

    print("\n---- Финальный ответ ----")
    print(last_msg.content)


#     Интеграция в продакшен
# Типичная архитектура:

# Клиент отправляет запрос → FastAPI получает user_id + сообщение
# Сервер загружает state из Redis/PostgreSQL по user_id
# Вызывается app.invoke(state)
# Обновлённое состояние сохраняется обратно в БД
# Клиент получает только финальный ответ (не всё состояние)
# Почему не передавать state в POST-запросе?

# Клиент может подделать task_id или историю сообщений
# Состояние может быть большим (сотни сообщений)
# Безопаснее и надёжнее хранить на сервере
# Пример (псевдокод):

# @app.post("/agent")
# async def handle_agent(user_id: str, query: str):
#     state = await db.get_state(user_id) or {"messages": [], "task_id": ""}
#     state["messages"].append(HumanMessage(content=query))
#     new_state = app.invoke(state)
#     await db.save_state(user_id, new_state)
#     return {"answer": new_state["messages"][-1].content}