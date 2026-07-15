from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/api/todos", response_model=list[schemas.TodoOut])
def list_todos(status: Optional[str] = None, db: Session = Depends(get_db)) -> list[schemas.TodoOut]:
    if status not in {None, "all", "active", "completed"}:
        raise HTTPException(status_code=422, detail="invalid status")
    todos = crud.get_todos(db, status=status if status != "all" else None)
    return todos


@app.post("/api/todos", response_model=schemas.TodoOut)
def create_todo(payload: schemas.TodoCreate, db: Session = Depends(get_db)) -> schemas.TodoOut:
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=422, detail="title is required")
    todo = crud.create_todo(db, payload.title)
    return todo


@app.patch("/api/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, payload: schemas.TodoUpdate, db: Session = Depends(get_db)) -> schemas.TodoOut:
    try:
        todo = crud.toggle_todo(db, todo_id, completed=payload.completed)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="todo not found") from exc
    return todo


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        crud.delete_todo(db, todo_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="todo not found") from exc
    return {"status": "deleted"}
