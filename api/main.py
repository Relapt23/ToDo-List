from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

from models import sessionmaker, create_engine, Base, ToDo, select, Tasks, InsertToDo, update, delete, CustomException, \
    Filter, UpdateTask, Status
from fastapi.templating import Jinja2Templates
from typing import List, Optional

engine = create_engine("sqlite:///database.db", echo=True)
sess = sessionmaker(engine)
engine.echo = False
Base.metadata.create_all(engine)
engine.echo = True

templates = Jinja2Templates(directory="templates")

app = FastAPI()


def get_session():
    with sess() as session:
        yield session


@app.get("/tasks", response_model=List[ToDo])
async def get_tasks(filter_status: Optional[Filter] = None, session: Session = Depends(get_session)):
    if filter_status == None or filter_status.value == "all":
        tasks = session.execute(select(Tasks)).scalars().all()
    else:
        tasks = session.execute(select(Tasks).where(filter_status.value == Tasks.status)).scalars().all()
    return tasks


@app.post("/tasks")
async def add_task(task: InsertToDo, session: Session = Depends(get_session)):
    new_task = Tasks(title=task.title, description=task.description, status=Status.todo.value)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@app.get("/tasks/{id}/")
async def get_current_task(id: int, session: Session = Depends(get_session)):
    current_task = session.execute(select(Tasks).where(id == Tasks.id)).scalar_one_or_none()
    if not current_task:
        raise CustomException(detail="not_found", status_code=404)
    return current_task


@app.put("/tasks/{id}/")
async def update_task(id: int, task: UpdateTask, session: Session = Depends(get_session)):
    current_task = session.execute(select(Tasks).where(id == Tasks.id)).scalar_one_or_none()
    if not current_task:
        raise CustomException(detail="not_found", status_code=404)
    session.execute(update(Tasks).where(id == Tasks.id).values(
        title=task.title, description=task.description, status=task.status))
    session.commit()
    session.refresh(current_task)
    return current_task


@app.delete("/tasks/{id}/")
async def delete_task(id: int, session: Session = Depends(get_session)):
    current_task = session.execute(select(Tasks).where(id == Tasks.id)).scalar_one_or_none()
    if not current_task:
        raise CustomException(detail="not_found", status_code=404)
    session.execute(delete(Tasks).where(id == Tasks.id))
    session.commit()
    return {"ok": True}
