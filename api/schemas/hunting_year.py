from pydantic import BaseModel, UUID4
from datetime import datetime

class HuntingYearRead(BaseModel):
    id: UUID4
    name: str
    is_current: bool
    start_date: datetime
    end_date: datetime
    
    model_config = {
        "from_attributes": True
    }