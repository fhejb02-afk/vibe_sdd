from typing import Optional

from sqlalchemy.orm import Session

from app.models import Todo


def create_todo(db: Session, title: str) -> Todo:
    todo = Todo(title=title.strip(), completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, status: Optional[str] = None) -> list[Todo]:
    query = db.query(Todo)
    if status == "active":
        query = query.filter(Todo.completed.is_(False))
    elif status == "completed":
        query = query.filter(Todo.completed.is_(True))
    return query.order_by(Todo.id.asc()).all()


def toggle_todo(db: Session, todo_id: int, completed: Optional[bool] = None) -> Todo:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise LookupError("todo not found")
    todo.completed = not todo.completed if completed is None else completed
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int) -> None:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise LookupError("todo not found")
    db.delete(todo)
    db.commit()
