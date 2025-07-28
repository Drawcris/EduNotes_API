from models.deadline import EventTypeEnum
from pydantic import BaseModel
from datetime import datetime
from models.deadline import EventTypeEnum

class ReadDeadline(BaseModel):
    deadline_id: int
    event_type: EventTypeEnum
    event_name: str
    event_description: str | None = None
    event_date: datetime
    organization_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime | None = None

class CreateDeadline(BaseModel):
    event_type: EventTypeEnum
    event_name: str
    event_description: str | None = None
    event_date: datetime
    organization_id: int

class UpdateDeadline(BaseModel):
    event_type: EventTypeEnum
    event_name: str
    event_description: str | None = None
    event_date: datetime
