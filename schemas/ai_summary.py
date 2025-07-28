from pydantic import BaseModel
from datetime import datetime
import models.ai_summary

class ReadAISummary(BaseModel):
    summary_id: int
    topic_id: int
    summary_text: str
    created_at: datetime
    updated_at: datetime | None = None
