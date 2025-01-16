from fastapi.responses import HTMLResponse
from fastapi import FastAPI, status
from fastapi.requests import Request
from models import sessionmaker, create_engine, Base, ToDo, select, Tasks, InsertToDo, update, delete, CustomException
from fastapi.templating import Jinja2Templates
from typing import List

engine = create_engine("sqlite:///database.db", echo=True)
sess = sessionmaker(engine)
engine.echo = False
Base.metadata.create_all(engine)
engine.echo = True

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/tasks", response_model=List[ToDo])
async def get_tasks():
    with sess() as session:
        tasks = session.execute(select(Tasks)).scalars().all()
    return tasks


@app.post("/tasks")
async def add_task(task: InsertToDo):
    with sess() as session:
        new_task = Tasks(title=task.title, description=task.description, status='todo')
        session.add(new_task)
        session.commit()
    return new_task


@app.get("/tasks/{id}/")
async def get_current_task(id: int):
    with sess() as session:
        current_task = session.execute(select(Tasks).where(id == Tasks.id)).scalar_one_or_none()
        if not current_task:
            raise CustomException(detail="Задачи с таким id не найдено", status_code=404)
        return current_task


@app.put("/tasks/{id}/")
async def update_task(id: int, task: ToDo):
    with sess() as session:
        current_task = session.execute(select(Tasks).where(id == Tasks.id)).scalar_one_or_none()
        if not current_task:
            raise CustomException(detail="Задачи с таким id не найдено", status_code=404)
        session.execute(update(Tasks).where(id == Tasks.id).values(
            title=task.title, description=task.description, status=task.status))
        session.commit()
        current_task = session.execute(select(Tasks).where(id == Tasks.id)).scalar_one_or_none()
    return current_task


@app.delete("/tasks/{id}/")
async def delete_task(id: int):
    with sess() as session:
        current_task = session.execute(select(Tasks).where(id == Tasks.id)).scalar_one_or_none()
        if not current_task:
            raise CustomException(detail="Задачи с таким id не найдено", status_code=404)
        session.execute(delete(Tasks).where(id == Tasks.id))
        session.commit()
    return current_task
