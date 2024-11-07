from pydantic import BaseModel
from typing import List, Optional


class NotificationContext(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    confirmation_link: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class NotificationRequest(BaseModel):
    service_name: str
    recipients: List[str]
    template_name: str
    context: NotificationContext

    model_config = {
        "from_attributes": True
    }
