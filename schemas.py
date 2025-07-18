from pydantic import BaseModel
from datetime import datetime

# User schemas
class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str

class ReadUsersResponse(BaseModel):
    user_id : int
    username: str
    email: str
    first_name: str
    last_name: str
    score: int

class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


# Organization schemas
class ReadOrganizationResponse(BaseModel):
    organization_id: int
    organization_name: str
    created_at: datetime
    updated_at: datetime | None = None

class CreateOrganizationRequest(BaseModel):
    organization_name: str

class UpdateOrganizationRequest(BaseModel):
    organization_name: str | None = None

