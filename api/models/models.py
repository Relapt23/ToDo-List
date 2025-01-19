from pydantic import BaseModel
from fastapi import HTTPException
from enum import Enum


class InsertTask(BaseModel):
    title: str
    description: str


class UpdateTask(BaseModel):
    title: str
    description: str
    status: str


class Task(BaseModel):
    title: str
    description: str
    status: str
    id: int


class Status(Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Filter(Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    all = "all"


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)
