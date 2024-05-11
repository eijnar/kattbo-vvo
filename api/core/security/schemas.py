from typing import Union

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
    
class User(BaseModel):
    username: str
    email: Union[str | None] = None
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    email: Union[str | None] = None
    disabled: Union[bool | None] = None
    
    
class UserInDB(User):
    hashed_password: str