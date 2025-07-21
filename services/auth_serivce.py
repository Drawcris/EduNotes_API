from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import db_dependency
from typing import Annotated
from datetime import datetime, timedelta, UTC
from fastapi import Depends, HTTPException, status
from models.user import User
from sqlalchemy import or_
import os

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(or_(User.username == username, User.email == username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user

def create_access_token(username: str, user_id: int, email: str, expires_delta: timedelta):
    encode = {'sub': username, 'user_id': user_id, 'email': email}
    expires = datetime.now(UTC) + expires_delta
    encode.update({'exp': int(expires.timestamp())})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        if username is None or user_id is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="could not validate credentials")

    return {"username": username, "user_id": user_id, "email": email}

user_dependency = Annotated[dict, Depends(get_current_user)]
