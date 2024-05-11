from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    roles: str
    
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    