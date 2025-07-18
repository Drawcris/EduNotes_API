from fastapi import APIRouter, HTTPException, status, Form
from models import OrganizationUser, UserRoleEnum
from database import db_dependency
from schemas import ReadOrganizationUserResponse


router = APIRouter(
    prefix="/organization_users",
    tags=["organization_users"],
)

@router.get("/", response_model=list[ReadOrganizationUserResponse])
async def read_users(db: db_dependency):
    users = db.query(OrganizationUser).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found in the organization")
    return [user for user in users]

@router.get("/{organization_id}", response_model=list[ReadOrganizationUserResponse])
async def read_organization_users(db: db_dependency, organization_id: int):
    users = db.query(OrganizationUser).filter_by(organization_id=organization_id).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found in the organization")
    return users

@router.post("/")
async def create_organization_user(
    db: db_dependency,
    organization_id: int,
    user_id: int,
    role: UserRoleEnum = Form(UserRoleEnum.user)
):
    existing_user = db.query(OrganizationUser).filter_by(organization_id=organization_id, user_id=user_id).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists in the organization")
    new_organization_user = OrganizationUser(
        organization_id=organization_id,
        user_id=user_id,
        role=role
    )
    db.add(new_organization_user)
    db.commit()
    db.refresh(new_organization_user)
    return {
        "Message": "Organization user created successfully",
        "user_id": user_id,
        "organization_id": organization_id,
        "role": role}

@router.delete("/{organization_id}/{user_id}")
async def delete_organization_user(
    db: db_dependency,
    organization_id: int,
    user_id: int
):
    organization_user = db.query(OrganizationUser).filter_by(organization_id=organization_id, user_id=user_id).first()
    if not organization_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the organization")
    db.delete(organization_user)
    db.commit()
    return {"message": f"User {user_id} removed from organization {organization_id} successfully"}