from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional
import re


def parse_duration(duration_str: str) -> timedelta:
    total_seconds = 0
    pattern = r'(\d+)([yMwdhms])'
    matches = re.findall(pattern, duration_str)
    if not matches:
        raise ValueError(
            "Invalid duration format. Use formats like '30d', '12h', '1h30m', etc.")
    for value, unit in matches:
        value = int(value)
        if unit == 'y':
            total_seconds += value * 365 * 24 * 3600
        elif unit == 'M':
            total_seconds += value * 30 * 24 * 3600
        elif unit == 'w':
            total_seconds += value * 7 * 24 * 3600
        elif unit == 'd':
            total_seconds += value * 24 * 3600
        elif unit == 'h':
            total_seconds += value * 3600
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 's':
            total_seconds += value
        else:
            raise ValueError(
                "Invalid time unit. Use 'y', 'M', 'w', 'd', 'h', 'm', or 's'.")
    return timedelta(seconds=total_seconds)


class APIKeyCreateSchema(BaseModel):
    permissions: List[str] = Field(...,
                                   description="List of permissions for the API Key")
    expires_in: Optional[timedelta] = Field(
        None, description="Expiration duration (e.g., '30d', '12h') for the API Key")

    @field_validator('expires_in', mode='before')
    def validate_expires_in(cls, v):
        if v is None:
            return None
        return parse_duration(v)


class APIKeyCreateResponseSchema(BaseModel):
    api_key: str
    identifier: str
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True



class APIKeyReadSchema(BaseModel):
    id: UUID
    created_at: datetime
    expires_at: Optional[datetime]
    permissions: List[str]
    revoked: bool

    class Config:
        from_attributes = True


class APIKeyRevokeResponseSchema(BaseModel):
    id: UUID
    identifier: Optional[str]
    revoked: bool
    revoked_at: datetime
    message: Optional[str]

    class Config:
        from_attributes = True
