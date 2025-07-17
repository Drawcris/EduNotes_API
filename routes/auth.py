from dotenv import load_dotenv
from datetime import timedelta, datetime, UTC
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from typing import Annotated, List
from schemas import CreateUserRequest, ReadUsersResponse, Token
from starlette import status
from database import db_dependency
from models import User
from sqlalchemy import or_
import os

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    user_model = User(username=create_user_request.username,
                email=create_user_request.email,
                password_hash=bcrypt_context.hash(create_user_request.password),
                first_name=create_user_request.first_name,
                last_name=create_user_request.last_name)
    existing_user = db.query(User).filter(or_(User.username == create_user_request.username,
                                          User.email == create_user_request.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username or email already exists")
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "User created successfully", "user_id": user_model.user_id, "username": user_model.username}
@router.post("/login", response_model=Token)
async def login_for_access_token(db: db_dependency,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    token = create_access_token(user.username, user.user_id, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(or_(User.username == username, User.email == username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'user_id': user_id}
    expires = datetime.now(UTC) + expires_delta
    encode.update({'exp': int(expires.timestamp())})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="could not validate credentials")

    return {"username": username, "user_id": user_id}

user_dependency = Annotated[dict, Depends(get_current_user)]
