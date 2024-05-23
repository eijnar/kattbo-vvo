from pydantic import BaseModel, EmailStr
from typing import List

class NotificationContext(BaseModel):
    first_name: str
    last_name: str = None
    confirmation_link: str = None

class NotificationRequest(BaseModel):
    service_name: str
    recipients: List[str]
    template_name: str
    context: NotificationContext