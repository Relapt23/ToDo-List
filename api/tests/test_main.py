from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from api.models.db_models import Base, Tasks
from api.main import app, get_session
from api.models.models import Status
from typing import List


def create_db() -> sessionmaker[Session]:
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
    return sess


client = TestClient(app)


def test_create_task():
    # given
    create_db()

    # when
    response = client.post(
        "/tasks", json={
            "title": "Пропылесосить",
            "description": "Пропылесосить кухню и коридор"
        }
    )

    # then
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Пропылесосить"
    assert data["description"] == "Пропылесосить кухню и коридор"
    assert data["status"] == "todo"
    assert data["id"] is not None


def test_get_task():
    # given
    sess = create_db()
    with sess() as session:
        new_task = Tasks(title="Сделать дз", description="Написать сочинение", status=Status.todo.value)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

    # when
    response = client.get("/tasks/"f"{new_task.id}")

    # then
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == new_task.id
    assert data["title"] == new_task.title
    assert data["description"] == new_task.description
    assert data["status"] == new_task.status


def test_get_filtered_tasks():
    # given
    tasks: List[Tasks] = [
        Tasks(title="Погулять", description="Погулять с собакой", status=Status.todo.value),
        Tasks(title="Погулять2", description="Погулять с собакой2", status=Status.in_progress.value),
        Tasks(title="Погулять3", description="Погулять с собакой3", status=Status.in_progress.value)
    ]
    sess = create_db()
    with sess() as session:
        for task in tasks:
            session.add(task)
        session.commit()
        for task in tasks:
            session.refresh(task)

    # when
    response = client.get("/tasks?filter_status=in_progress")

    # then
    assert response.status_code == 200
    data = response.json()
    filtered_tasks = filter(lambda x: x.status == Status.in_progress.value, tasks)
    for i, task in enumerate(filtered_tasks):
        assert data[i]["title"] == task.title
        assert data[i]["description"] == task.description
        assert data[i]["status"] == task.status
        assert data[i]["id"] == task.id
