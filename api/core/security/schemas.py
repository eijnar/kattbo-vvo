from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None


class TokenDataSchema(BaseModel):
    user_id: int | None = None
    scopes: list[str] = []
