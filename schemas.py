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
    avatar_url: str | None = None

class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

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


# Channel schemas
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

# Topic schemas
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


# Note schemas
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


# Organization User schemas
class ReadOrganizationUserResponse(BaseModel):
    organization_id: int
    user_id: int
    role: str
    updated_at: datetime | None = None


