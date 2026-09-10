def build_system_prompt(task_id: str) -> str:
    if task_id.strip():
        return f"Ты — агент управления задачами. Текущий task_id: {task_id}. Если задача не создана — сначала вызови create_task. Не выдумывай ID."
    else:
        return f"Ты — агент управления задачами. Текущий task_id: не задан. Если задача не создана — сначала вызови create_task. Не выдумывай ID."