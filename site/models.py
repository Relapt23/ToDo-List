from pydantic import BaseModel
from fastapi import Form
from enum import Enum


class CreateTask(BaseModel):
    title: str
    description: str

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
            description: str = Form(...),
    ):
        return cls(title=title, description=description)


class UpdateTask(BaseModel):
    title: str
    description: str
    status: str

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
            description: str = Form(...),
            status: str = Form(...),
    ):
        return cls(title=title, description=description, status=status)


class Status(Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Filter(Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    all = "all"

    def display_name(self):
        filter_to_string = {
            Filter.all: "Все",
            Filter.todo: "ToDo",
            Filter.in_progress: "In Progress",
            Filter.done: "Done"
        }
        return filter_to_string[self]
