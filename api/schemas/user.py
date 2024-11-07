from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    disabled: Optional[bool] = None

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

    @model_validator(mode='after')
    def check_required_fields(cls, values):
        required_fields = ['first_name', 'last_name']
        missing_fields = [
            field for field in required_fields if not values.get(field)]
        if missing_fields:
            raise ValueError(
                f"Missing required fields: {', '.join(missing_fields)}")
        return values

    model_config = {
        "from_attributes": True
    }
