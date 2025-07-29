from fastapi import APIRouter, HTTPException, status, Form

from models.organization import Organization
from models.organization_user import OrganizationUser, UserRoleEnum
from models.notifications import Notification
from database import db_dependency
from schemas.organization_user import ReadOrganizationUserResponse
from schemas.responses import StandardResponse
from services.auth_serivce import user_dependency
from models.user import User


router = APIRouter(
    prefix="/organization_users",
    tags=["organization_users"],
)

@router.get("/me", response_model=StandardResponse[list[ReadOrganizationUserResponse]])
async def get_current_user_organizations(
    user: user_dependency,
    db: db_dependency
):
    organization_users = db.query(OrganizationUser).filter_by(user_id=user["user_id"]).all()
    if not organization_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not part of any organization")
    return StandardResponse(
        success=True,
        message="User organizations retrieved successfully",
        data=organization_users
    )

@router.get("/{organization_id}/{user_id}/role", response_model=StandardResponse[dict])
async def get_user_role(db: db_dependency, organization_id: int, user_id: int):
    org_user = db.query(OrganizationUser).filter_by(organization_id=organization_id, user_id=user_id).first()
    if not org_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the organization")
    return StandardResponse(
        success=True,
        message="User role retrieved successfully",
        data={"role": org_user.role, "organization_id": organization_id, "user_id": user_id}
    )


@router.post("/invite", response_model=StandardResponse[dict])
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
    return StandardResponse(
        success=True,
        message="User invited to organization successfully",
        data={
            "user_id": invited_user_id,
            "organization_id": organization_id,
            "role": role
        }
    )

@router.delete("/RemoveUserFromOrganization", response_model=StandardResponse[ReadOrganizationUserResponse])
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

    organization = db.query(Organization).filter_by(organization_id=organization_id).first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    organization_user = db.query(OrganizationUser).filter_by(
        organization_id=organization_id,
        user_id=user_id
    ).first()
    if not organization_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the organization")

    db.delete(organization_user)
    db.commit()

    notification = Notification(user_id=user_id, message=f"You have been removed from organization {organization.organization_name}.", status="unread")
    db.add(notification)
    db.commit()

    return StandardResponse(
        success=True,
        message=f"User {user_id} removed from organization {organization_id} successfully",
        data=None
    )

@router.put("/{organization_id}/{user_id}/role", response_model=StandardResponse[dict])
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
    return StandardResponse(
        success=True,
        message="User role updated successfully",
        data={
            "user_id": user_id,
            "organization_id": organization_id,
            "role": role
        }
    )

# CRUD

@router.get("/", response_model=StandardResponse[list[ReadOrganizationUserResponse]])
async def read_users(db: db_dependency):
    users = db.query(OrganizationUser).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found in the organization")
    return StandardResponse(
        success=True,
        message="Organization users retrieved successfully",
        data=users
    )

@router.get("/{organization_id}", response_model=StandardResponse[list[ReadOrganizationUserResponse]])
async def read_organization_user(db: db_dependency, organization_id: int):
    users = db.query(OrganizationUser).filter_by(organization_id=organization_id).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found in the organization")
    return StandardResponse(
        success=True,
        message="Organization users retrieved successfully",
        data=users
    )

@router.post("/", response_model=StandardResponse[ReadOrganizationUserResponse])
async def create_organization_user(
    db: db_dependency,
    organization_id: int,
    user_id: int,
    role: UserRoleEnum = Form(UserRoleEnum.user)
):
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
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
    return StandardResponse(
        success=True,
        message="Organization user created successfully",
        data=new_organization_user
    )

@router.delete("/{organization_id}/{user_id}", response_model=StandardResponse)
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
    return StandardResponse(
        success=True,
        message="Organization user deleted successfully",
        data=None
    )
