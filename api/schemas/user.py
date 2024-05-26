from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    auth0_id: str
    email: str
    first_name: str

    class Config:
        orm_mode: True