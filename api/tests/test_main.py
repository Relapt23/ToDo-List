from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from api.models.db_models import Base
from api.main import app, get_session


def create_db():
    engine = create_engine(
        "sqlite:///testing.db", connect_args={"check_same_thread": False}
    )
    sess = sessionmaker(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with sess() as session:
        def get_session_override():
            return session

    app.dependency_overrides[get_session] = get_session_override


client = TestClient(app)


def test_create_task():
    create_db()
    response = client.post("/tasks", json={"title": "Пропылесосить", "description": "Пропылесосить кухню и коридор"})
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Пропылесосить"
    assert data["description"] == "Пропылесосить кухню и коридор"
    assert data["status"] == "todo"
    assert data["id"] is not None


def test_get_task():
    create_db()
    response = client.post("/tasks", json={"title": "Сделать домашнее задание", "description": "Написать сочинение"})
    data = response.json()
    id = data["id"]
    response = client.get("/tasks/"f"{id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == id
    assert data["title"] == "Сделать домашнее задание"
    assert data["description"] == "Написать сочинение"
    assert data["status"] == "todo"


def test_get_filtered_tasks():
    create_db()
    response = client.post("/tasks", json={"title": "Помыть посуду", "description": "Помыть посуду и выкинуть мусор"})
    data = response.json()
    id = data["id"]
    client.put(
        "/tasks/"f"{id}",
        json={
            "title": "Помыть посуду",
            "description": "Помыть посуду и выкинуть мусор",
            "status": "done"
        }
    )
    response = client.get("/tasks?filter_status=done")
    assert response.status_code == 200
    assert {"title": "Помыть посуду", "description": "Помыть посуду и выкинуть мусор",
            "status": "done"}
