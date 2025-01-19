from pydantic import BaseModel
from sqlalchemy import select, delete, insert, update, create_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase
from typing import Optional
from fastapi import HTTPException
from enum import Enum


class InsertToDo(BaseModel):
    title: str
    description: str


class UpdateTask(BaseModel):
    title: str
    description: str
    status: str


class ToDo(BaseModel):
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


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str]
