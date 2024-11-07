from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from enum import Enum


class TaskType(str, Enum):
    payment = "payment"
    shooting_certificate = "shooting_certificate"


class TaskTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_mandatory: bool = False
    task_type: TaskType
    is_default: bool = False

    model_config = {
        "from_attributes": True
    }


class TaskTemplateCreate(TaskTemplateBase):
    pass


class TaskTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Task Name")
    description: Optional[str] = Field(None, example="Updated description")
    is_mandatory: Optional[bool] = Field(None, example=True)
    task_type: Optional[TaskType] = None
    is_default: Optional[bool] = Field(None, example=True)

    model_config = {
        "from_attributes": True
    }


class TaskTemplateRead(TaskTemplateBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }
