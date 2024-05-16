from pydantic import BaseModel

class ScopeBaseSchema(BaseModel):
    name: str
    description: str


class ScopeSchema(ScopeBaseSchema):
    id: int

    class Config:
        from_attributes = True

