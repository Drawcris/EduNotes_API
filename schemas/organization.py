from pydantic import BaseModel
from datetime import datetime

class ReadOrganizationResponse(BaseModel):
    organization_id: int
    organization_name: str
    created_at: datetime
    updated_at: datetime | None = None

class CreateOrganizationRequest(BaseModel):
    organization_name: str

class UpdateOrganizationRequest(BaseModel):
    organization_name: str | None = None
