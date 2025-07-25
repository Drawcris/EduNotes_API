from datetime import datetime
from pydantic import BaseModel

class ReadOrganizationUserResponse(BaseModel):
    organization_id: int
    user_id: int
    role: str
    updated_at: datetime | None = None


