from fastapi import FastAPI, Depends, status
from fastapi.templating import Jinja2Templates
import requests
import json
from models import ToDo, UpdateTask
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_todo(request: Request):
    response = requests.get('http://api:8000/tasks')
    tasks_list = json.loads(response.content.decode('utf-8'))

    return templates.TemplateResponse(name="tasks_list.html", context={"request": request, "tasks": tasks_list})


@app.post("/")
async def post_todo(todo: ToDo = Depends(ToDo.as_form)):
    requests.post('http://api:8000/tasks', json={"title": todo.title, "description": todo.description})
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/delete/{task_id}")
async def delete_todo(task_id: int):
    requests.delete(f'http://api:8000/tasks/{task_id}/')
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/edit/{task_id}")
async def post_todo(task_id: int, todo: UpdateTask = Depends(UpdateTask.as_form)):
    response = requests.put(f'http://api:8000/tasks/{task_id}/',
                            json={"title": todo.title, "description": todo.description, "status": todo.status})
    print(json.loads(response.content.decode('utf-8')))
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{task_id}")
async def get_todo(task_id: int, request: Request):
    response = requests.get(f'http://api:8000/tasks/{task_id}/')
    task = json.loads(response.content.decode('utf-8'))
    return templates.TemplateResponse(name="edit_task.html", context={"request": request, "task": task})
