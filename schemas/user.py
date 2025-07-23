from pydantic import BaseModel
from models.user import RankEnum

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
    rank: RankEnum

class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str