from uuid import UUID
from pydantic import BaseModel, model_validator
from typing import Optional

class UserBaseSchema(BaseModel):
    id: UUID
    email: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    disabled: bool | None = None

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    auth0_id: str
    email: str
    phone_number: str

    class Config:
        orm_mode: True
        
class UserUpdateSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    
    @model_validator(mode='after')
    def check_required_fields(cls, values):
        required_fields = ['first_name', 'last_name']
        missing_fields = [field for field in required_fields if not getattr(values, field, None)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        return values
    
    class Config:
        orm_mode: True