from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID

from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    uuid: UUID

    model_config = ConfigDict(from_attributes=True)


class TaskDelete(BaseModel):
    uuid: UUID
