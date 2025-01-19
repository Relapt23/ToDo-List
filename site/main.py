from fastapi import FastAPI, Depends, status
from fastapi.templating import Jinja2Templates
import requests
import json
from models import CreateTask, UpdateTask, Filter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_tasks(request: Request, filter_status: Filter = Filter.all):
    if filter_status.value != "all":
        response = requests.get(f'http://api:8000/tasks?filter_status={filter_status.value}')
    else:
        response = requests.get('http://api:8000/tasks')

    if response.status_code == 200:
        tasks_list = json.loads(response.content.decode('utf-8'))
    else:
        tasks_list = []

    return templates.TemplateResponse(
        name="tasks_list.html",
        context={
            "request": request,
            "tasks": tasks_list,
            "filter": filter_status.display_name()
        }
    )


@app.post("/")
async def post_task(todo: CreateTask = Depends(CreateTask.as_form)):
    requests.post(
        'http://api:8000/tasks',
        json={
            "title": todo.title,
            "description": todo.description
        }
    )
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/delete/{task_id}")
async def delete_task(task_id: int):
    requests.delete(f'http://api:8000/tasks/{task_id}/')
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/edit/{task_id}")
async def edit_task(task_id: int, todo: UpdateTask = Depends(UpdateTask.as_form)):
    requests.put(
        f'http://api:8000/tasks/{task_id}/',
        json={
            "title": todo.title,
            "description": todo.description,
            "status": todo.status
        }
    )
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{task_id}")
async def edit_task(task_id: int, request: Request):
    response = requests.get(f'http://api:8000/tasks/{task_id}/')
    task = json.loads(response.content.decode('utf-8'))
    return templates.TemplateResponse(name="edit_task.html", context={"request": request, "task": task})
