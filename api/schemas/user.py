from pydantic import BaseModel, EmailStr
from typing import List

class UserBaseSchema(BaseModel):
    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str
