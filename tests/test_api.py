import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import Todo


@pytest.fixture(autouse=True)
def clear_db():
    db = SessionLocal()
    db.query(Todo).delete()
    db.commit()
    db.close()
    yield
    db = SessionLocal()
    db.query(Todo).delete()
    db.commit()
    db.close()


client = TestClient(app)


def test_create_todo_and_list_it():
    response = client.post("/api/todos", json={"title": "테스트 할 일"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "테스트 할 일"
    assert data["completed"] is False

    list_response = client.get("/api/todos")
    assert list_response.status_code == 200
    assert any(item["title"] == "테스트 할 일" for item in list_response.json())


def test_create_todo_with_empty_title_returns_422():
    response = client.post("/api/todos", json={"title": "   "})
    assert response.status_code == 422


def test_toggle_todo_and_delete_it():
    create_response = client.post("/api/todos", json={"title": "토글 테스트"})
    todo_id = create_response.json()["id"]

    toggle_response = client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    assert toggle_response.status_code == 200
    assert toggle_response.json()["completed"] is True

    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200

    missing_response = client.delete(f"/api/todos/{todo_id}")
    assert missing_response.status_code == 404


def test_filter_and_remaining_count():
    client.post("/api/todos", json={"title": "필터 1"})
    client.post("/api/todos", json={"title": "필터 2"})

    created = client.get("/api/todos")
    items = created.json()
    active_id = next(item["id"] for item in items if item["title"] == "필터 1")
    client.patch(f"/api/todos/{active_id}", json={"completed": True})

    active_response = client.get("/api/todos?status=active")
    completed_response = client.get("/api/todos?status=completed")
    all_response = client.get("/api/todos?status=all")

    assert active_response.status_code == 200
    assert completed_response.status_code == 200
    assert all_response.status_code == 200
    assert len(active_response.json()) == 1
    assert len(completed_response.json()) == 1
    assert len(all_response.json()) == 2


def test_health_and_root_page():
    health_response = client.get("/health")
    root_response = client.get("/")

    assert health_response.status_code == 200
    assert root_response.status_code == 200
