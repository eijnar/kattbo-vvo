from pydantic import BaseModel
from typing import List

from .scope import ScopeSchema

class RoleBaseSchema(BaseModel):
    name: str
    description: str

class RoleWithScopes(RoleBaseSchema):
    id: int
    scopes: List[ScopeSchema]

    class Config:
        from_attributes = True