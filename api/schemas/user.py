from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }


class UserCreate(UserBase):
    auth0_id: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(
        None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    phone_number: Optional[str] = Field(
        None, description="Phone number of the user")

    model_config = {
        "from_attributes": True
    }
