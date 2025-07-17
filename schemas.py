from pydantic import BaseModel

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

class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str