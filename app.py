from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Имитация базы данных в памяти
tasks = [
    {"id": 1, "title": "Изучить основы маршрутизации в Flask", "done": True},
    {"id": 2, "title": "Разобраться с шаблонизатором Jinja2", "done": False},
]

@app.route("/", methods=["GET", "POST"])
def index():
    # Если пользователь отправил форму (добавление задачи)
    if request.method == "POST":
        task_title = request.form.get("title")
        if task_title:  # Проверка, что поле не пустое
            new_id = max([t["id"] for t in tasks], default=0) + 1
            tasks.append({"id": new_id, "title": task_title, "done": False})
        return redirect(url_for("index"))

    # При обычном открытии страницы (GET) отдаем HTML-шаблон
    return render_template("index.html", tasks=tasks)

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    # Изменение статуса задачи (выполнено / не выполнено)
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    # Удаление задачи по её ID
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

# Простой API-эндпоинт для тестирования возврата JSON
@app.route("/api/tasks")
def api_tasks():
    return {"tasks": tasks, "total": len(tasks)}

if __name__ == "__main__":
    # debug=True автоматически перезагружает сервер при изменении кода
    app.run(debug=True)