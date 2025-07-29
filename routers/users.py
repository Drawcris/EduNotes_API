from fastapi import APIRouter, HTTPException, status, Form, Depends, File, UploadFile
from schemas.user import ReadUsersResponse, UpdateUserRequest
from database import db_dependency
from models.user import User
from models.organization_invitations import OrganizationInvitation
from passlib.context import CryptContext
from uuid import uuid4
from services.auth_serivce import user_dependency
from schemas.responses import StandardResponse
import os

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.put("/{user_id}/change_password")
async def change_password(user: user_dependency, db: db_dependency,
                          old_password: str = Form(...), new_password: str = Form(...)):
    user = db.query(User).filter(User.user_id == user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    user.password_hash = bcrypt_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return StandardResponse(
        success=True,
        message=f"Password changed successfully",
    )

@router.put("/{user_id}/avatar")
async def update_user_avatar(db: db_dependency, user: user_dependency, file: UploadFile = File(...)):
    target_user = db.query(User).filter(User.user_id == user["user_id"]).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user["user_id"] != target_user.user_id:
        raise HTTPException(status_code=403, detail="You can only update your own avatar")
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join("media", "avatars", filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    target_user.avatar_url = f"/media/avatars/{filename}"
    db.commit()
    db.refresh(target_user)
    return StandardResponse(
        success=True,
        message=f"Avatar updated successfully",
        data={"avatar_url": target_user.avatar_url}
    )

# CRUD

@router.get("/", response_model=StandardResponse[list[ReadUsersResponse]])
async def read_users(db: db_dependency):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return StandardResponse(
        success=True,
        message="Users retrieved successfully",
        data=[user for user in users]
    )

@router.get("/{user_id}", response_model=StandardResponse[ReadUsersResponse])
async def read_user(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return StandardResponse(
        success=True,
        message="User retrieved successfully",
        data=user
    )

@router.delete("/{user_id}", response_model=StandardResponse[ReadUsersResponse])
async def delete_user(user: user_dependency, db: db_dependency):
    user_to_delete = db.query(User).filter(User.user_id == user["user_id"]).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(OrganizationInvitation).filter(
        OrganizationInvitation.invited_by_user_id == user["user_id"]
    ).delete()
    db.delete(user_to_delete)
    db.commit()
    return StandardResponse(
        success=True,
        message=f"User deleted successfully",
        data=user_to_delete
    )
@router.put("/{user_id}", response_model=StandardResponse[ReadUsersResponse])
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
    return StandardResponse(
        success=True,
        message="User updated successfully",
        data=user_to_update
    )

