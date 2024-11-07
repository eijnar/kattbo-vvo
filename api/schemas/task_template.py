from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from enum import Enum


class TaskType(str, Enum):
    payment = "payment"
    shooting_certificate = "shooting_certificate"


class TaskTemplateCreate(BaseModel):
    name: str = Field(..., example="Avgift 1")
    description: Optional[str] = Field(None, example="Första betalningen")
    is_mandatory: bool = Field(..., example=True)
    task_type: TaskType
    is_default: bool = Field(False, example=True)


class TaskTemplateRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    is_mandatory: bool
    task_type: TaskType
    is_default: bool

    model_config = {
        "from_attributes": True
    }


class TaskTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Avgift 1 updaterad")
    description: Optional[str] = Field(
        None, example="Uppdaterat beskrivningen")
    is_mandatory: Optional[bool] = Field(None, example=False)
    task_type: Optional[TaskType]
    is_default: Optional[bool] = Field(None, example=True)
