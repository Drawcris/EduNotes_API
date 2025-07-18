from fastapi import APIRouter, HTTPException, status, Form
from models import OrganizationUser, UserRoleEnum
from database import db_dependency
from schemas import ReadOrganizationUserResponse
from routes.auth import user_dependency


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

@router.get("/{organization_id}/{user_id}/role")
async def get_user_role(db: db_dependency, organization_id: int, user_id: int):
    org_user = db.query(OrganizationUser).filter_by(organization_id=organization_id, user_id=user_id).first()
    if not org_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the organization")
    return {"role": org_user.role}

@router.post("/invite")
async def invite_user_to_organization(
    user: user_dependency,
    db: db_dependency,
    organization_id: int,
    invited_user_id: int,
    role: UserRoleEnum = Form(UserRoleEnum.user)
):
    org_user = db.query(OrganizationUser).filter_by(
        organization_id=organization_id,
        user_id=user["user_id"]
    ).first()
    if not org_user or org_user.role != UserRoleEnum.owner:
        raise HTTPException(status_code=403, detail="No permission to invite users to this organization")

    # Dodaj nowego użytkownika do organizacji
    existing_user = db.query(OrganizationUser).filter_by(
        organization_id=organization_id,
        user_id=invited_user_id
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists in the organization")

    new_organization_user = OrganizationUser(
        organization_id=organization_id,
        user_id=invited_user_id,
        role=role
    )
    db.add(new_organization_user)
    db.commit()
    db.refresh(new_organization_user)
    return {"message": "User invited to organization successfully",}

@router.delete("/RemoveUserFromOrganization")
async def remove_user_from_organization(
    user: user_dependency,
    db: db_dependency,
    organization_id: int,
    user_id: int
):
    org_user = db.query(OrganizationUser).filter_by(
        organization_id=organization_id,
        user_id=user["user_id"]
    ).first()
    if not org_user or org_user.role != UserRoleEnum.owner:
        raise HTTPException(status_code=403, detail="No permission to remove users from this organization")

    organization_user = db.query(OrganizationUser).filter_by(
        organization_id=organization_id,
        user_id=user_id
    ).first()
    if not organization_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the organization")

    db.delete(organization_user)
    db.commit()
    return {"message": f"User {user_id} removed from organization {organization_id} successfully"}

@router.put("/{organization_id}/{user_id}/role")
async def update_user_role(
    db: db_dependency,
    organization_id: int,
    user_id: int,
    role: UserRoleEnum = Form(UserRoleEnum.user)
):
    organization_user = db.query(OrganizationUser).filter_by(
        organization_id=organization_id, user_id=user_id
    ).first()
    if not organization_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the organization")

    organization_user.role = role
    db.commit()
    return {"message": f"User {user_id} role updated to {role} in organization {organization_id}"}