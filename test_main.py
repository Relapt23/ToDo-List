from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
from main import app, get_session


def test_create_db():
    engine = create_engine(
        "sqlite:///testing.db", connect_args={"check_same_thread": False}
    )
    sess = sessionmaker(engine)
    Base.metadata.create_all(engine)

    with sess() as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)
        response = client.post("/tasks",
                               json={"title": "Пропылесосить", "description": "Пропылесосить кухню и коридор"}
                               )
        app.dependency_overrides.clear()
        data = response.json()
        assert response.status_code == 200
        assert data["title"] == "Пропылесосить"
        assert data["description"] == "Пропылесосить кухню и коридор"
        assert data["status"] == "todo"
        assert data["id"] is not None

        client.post("/tasks", json={"title": "Сделать домашнее задание", "description": "Написать сочинение"})
        response = client.get("/tasks/14")
        app.dependency_overrides.clear()
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == 14
        assert data["title"] == "Сделать домашнее задание"
        assert data["description"] == "Написать сочинение"
        assert data["status"] == "in_progress"

        client.put("/tasks/18/",
                   json={"title": "Сделать домашнее задание", "description": "Написать сочинение",
                         "status": "done"})
        response = client.get("/tasks?filterStatus=done")
        app.dependency_overrides.clear()
        data = response.json()
        assert response.status_code == 200
        assert {"title": "Сделать домашнее задание", "description": "Написать сочинение",
                "status": "done"}
