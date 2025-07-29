from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from starlette import status
from database import db_dependency
from models.user import User
from sqlalchemy import or_
from schemas.auth import Token
from schemas.user import CreateUserRequest, ReadUsersResponse
from schemas.responses import StandardResponse
from services.auth_serivce import authenticate_user, create_access_token, bcrypt_context


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=StandardResponse[ReadUsersResponse])
async def create_user(db: db_dependency,
                     create_user_request: CreateUserRequest):
    user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        password_hash=bcrypt_context.hash(create_user_request.password),
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name
    )
    existing_user = db.query(User).filter(
        or_(User.username == create_user_request.username,
            User.email == create_user_request.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return StandardResponse(
        success=True,
        message="User registered successfully",
        data=user_model
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(db: db_dependency,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    token = create_access_token(user.username, user.user_id, user.email, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}

