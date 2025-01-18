from pydantic import BaseModel
from fastapi import Form
from enum import Enum


class ToDo(BaseModel):
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