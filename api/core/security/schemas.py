from typing import Union, List

from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class TokenDataSchema(BaseModel):
    user_id: int | None = None
    scopes: list[str] = []


class RoleBaseSchema(BaseModel):
    name: str
    description: str


class ScopeBaseSchema(BaseModel):
    name: str
    description: str


class ScopeSchema(ScopeBaseSchema):
    id: int

    class Config:
        from_attributes = True


class RoleWithScopes(RoleBaseSchema):
    id: int
    scopes: List[ScopeSchema]

    class Config:
        from_attributes = True


class UserBaseSchema(BaseModel):
    id: int
    email: str
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    disabled: Union[bool | None] = None

    class Config:
        from_attributes = True


class NewUserSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str
