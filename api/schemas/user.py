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
    sub: str
    nickname: str
    name: str
    picture: str
    updated_at: str

    class Config:
        orm_mode: True