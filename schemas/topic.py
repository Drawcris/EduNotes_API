from pydantic import BaseModel
from datetime import datetime

class ReadTopicResponse(BaseModel):
    topic_id: int
    topic_name: str
    channel_id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime | None = None

class CreateTopicRequest(BaseModel):
    topic_name: str
    channel_id: int
    organization_id: int

class UpdateTopicNameRequest(BaseModel):
    topic_name: str

class UpdateTopicRequest(BaseModel):
    topic_name: str | None = None
    channel_id: int | None = None
    organization_id: int | None = None
