from pydantic import BaseModel
from datetime import datetime

class ReadNotifications(BaseModel):
    notification_id: int
    user_id: int
    status: str
    message: str
    created_at: datetime