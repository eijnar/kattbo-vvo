from pydantic import BaseModel, Field, HttpUrl


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None


class TokenDataSchema(BaseModel):
    user_id: int | None = None
    scopes: list[str] = []

class ClientBase(BaseModel):
    client_id: str = Field(..., example="my_client_id")
    redirect_uri: HttpUrl = Field(..., example="https://example.com/callback")
    name: str = Field(..., example="My Application")
    description: str = Field(None, example="A description of the client")

class ClientCreate(ClientBase):
    client_secret: str = Field(..., example="my_client_secret")

class ClientUpdate(ClientBase):
    client_secret: str = Field(None, example="new_client_secret")

class ClientInDB(ClientBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True