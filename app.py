from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TodoItem(BaseModel):
    id: int
    text: str
    done: bool

class CreateTodo(BaseModel):
    text: str

todos: List[TodoItem] = []
next_id = 1

@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>오늘의 할 일</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 720px; margin: 0 auto; padding: 24px; background: #f8fafc; color: #111827; }
        h1 { margin-bottom: 8px; }
        form { display: flex; gap: 10px; margin-bottom: 16px; }
        input[type=text] { flex: 1; padding: 10px; font-size: 16px; border: 1px solid #d1d5db; border-radius: 8px; }
        button { padding: 10px 16px; font-size: 16px; border: none; border-radius: 8px; background: #2563eb; color: white; cursor: pointer; }
        button:hover { background: #1d4ed8; }
        ul { list-style: none; padding: 0; margin: 0; }
        li { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; margin-bottom: 10px; border-radius: 12px; background: white; border: 1px solid #e5e7eb; }
        .todo-text { flex: 1; margin-right: 16px; word-break: break-word; }
        .todo-done { text-decoration: line-through; color: #6b7280; }
        .actions button { margin-left: 8px; }
        .empty { color: #6b7280; text-align: center; padding: 24px 0; }
    </style>
</head>
<body>
    <h1>오늘의 할 일</h1>
    <p>할 일을 입력하고 추가해보세요.</p>

    <form id="todo-form">
        <input id="todo-input" type="text" placeholder="할 일을 입력하세요" autocomplete="off" required />
        <button type="submit">추가</button>
    </form>

    <ul id="todo-list"></ul>
    <p id="empty-text" class="empty">할 일이 없습니다.</p>

    <script>
        const todoForm = document.getElementById('todo-form');
        const todoInput = document.getElementById('todo-input');
        const todoList = document.getElementById('todo-list');
        const emptyText = document.getElementById('empty-text');

        async function fetchTodos() {
            const response = await fetch('/api/todos');
            const todos = await response.json();
            renderTodos(todos);
        }

        function renderTodos(todos) {
            todoList.innerHTML = '';
            if (todos.length === 0) {
                emptyText.style.display = 'block';
                return;
            }
            emptyText.style.display = 'none';

            todos.forEach(todo => {
                const li = document.createElement('li');
                const textDiv = document.createElement('div');
                textDiv.className = 'todo-text';
                textDiv.textContent = todo.text;
                if (todo.done) {
                    textDiv.classList.add('todo-done');
                }

                const actions = document.createElement('div');
                actions.className = 'actions';

                const toggleButton = document.createElement('button');
                toggleButton.textContent = todo.done ? '취소' : '완료';
                toggleButton.onclick = async () => {
                    await fetch(`/api/todos/${todo.id}/toggle`, { method: 'POST' });
                    fetchTodos();
                };

                const deleteButton = document.createElement('button');
                deleteButton.textContent = '삭제';
                deleteButton.style.background = '#ef4444';
                deleteButton.style.color = 'white';
                deleteButton.onclick = async () => {
                    await fetch(`/api/todos/${todo.id}`, { method: 'DELETE' });
                    fetchTodos();
                };

                actions.appendChild(toggleButton);
                actions.appendChild(deleteButton);
                li.appendChild(textDiv);
                li.appendChild(actions);
                todoList.appendChild(li);
            });
        }

        todoForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text = todoInput.value.trim();
            if (!text) return;
            await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            todoInput.value = '';
            fetchTodos();
        });

        fetchTodos();
    </script>
</body>
</html>
"""

@app.get("/api/todos", response_model=List[TodoItem])
def get_todos() -> List[TodoItem]:
    return todos

@app.post("/api/todos", response_model=TodoItem)
def add_todo(item: CreateTodo) -> TodoItem:
    global next_id
    todo = TodoItem(id=next_id, text=item.text.strip(), done=False)
    next_id += 1
    todos.append(todo)
    return todo

@app.post("/api/todos/{todo_id}/toggle", response_model=TodoItem)
def toggle_todo(todo_id: int) -> TodoItem:
    for todo in todos:
        if todo.id == todo_id:
            todo.done = not todo.done
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {'status': 'ok'}
    raise HTTPException(status_code=404, detail='Todo not found')
