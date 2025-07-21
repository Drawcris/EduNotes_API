from datetime import datetime
from pydantic import BaseModel

class ReadChannelResponse(BaseModel):
    channel_id: int
    channel_name: str
    organization_id: int
    created_at: datetime
    updated_at: datetime | None = None

class CreateChannelRequest(BaseModel):
    channel_name: str
    organization_id: int

class UpdateChannelRequest(BaseModel):
    channel_name: str | None = None