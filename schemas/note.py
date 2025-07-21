from pydantic import BaseModel
from datetime import datetime

class ReadNoteResponse(BaseModel):
    note_id: int
    title: str
    topic_id: int
    organization_id: int
    user_id: int
    content_type: str
    content: str | None = None
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime | None = None



class CreateNoteRequest(BaseModel):
    tittle: str
    topic_id: int
    organization_id: int
    user_id: int
    content_type: str
    content: str | None = None
    image_url: str | None = None