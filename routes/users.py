from fastapi import APIRouter, HTTPException, status, Form, Depends
from schemas import ReadUsersResponse, UpdateUserRequest
from database import db_dependency
from models import User
from passlib.context import CryptContext
from routes.auth import user_dependency

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=list[ReadUsersResponse])
async def read_users(db: db_dependency):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return [user for user in users]

@router.get("/{user_id}", response_model=ReadUsersResponse)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user: user_dependency, user_id: int, db: db_dependency):
    user_to_delete = db.query(User).filter(User.user_id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_to_delete)
    db.commit()
    return {"message": f"User {user_to_delete.username} deleted successfully"}

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: UpdateUserRequest,
    db: db_dependency
):
    user_to_update = db.query(User).filter(User.user_id == user_id).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.username is not None:
        user_to_update.username = user_update.username
    if user_update.email is not None:
        user_to_update.email = user_update.email
    if user_update.first_name is not None:
        user_to_update.first_name = user_update.first_name
    if user_update.last_name is not None:
        user_to_update.last_name = user_update.last_name
    if user_update.password:
        user_to_update.password_hash = bcrypt_context.hash(user_update.password)
    db.commit()
    db.refresh(user_to_update)
    return {"message": f"User {user_to_update.username} updated successfully"}
