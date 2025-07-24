from fastapi import APIRouter, HTTPException, status
from models.organization import Organization
from database import db_dependency
from schemas.organization import ReadOrganizationResponse, CreateOrganizationRequest, UpdateOrganizationRequest
from datetime import datetime, UTC
from services.auth_serivce import user_dependency
from models.organization_user import OrganizationUser, UserRoleEnum

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)

@router.get("/my")
async def read_my_organizations(user: user_dependency, db: db_dependency):
    user_id = user["user_id"]
    organizations = (db.query(Organization).
                     join(OrganizationUser).
                     filter(OrganizationUser.user_id == user_id).all())
    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No organizations found for this user")
    return [organization for organization in organizations]

# CRUD

@router.get("/", response_model=list[ReadOrganizationResponse])
async def read_organizations(db: db_dependency):
    organizations = db.query(Organization).all()
    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No organizations found")
    return [organization for organization in organizations]

@router.get("/{organization_id}", response_model=ReadOrganizationResponse)
async def read_organization(organization_id: int, db: db_dependency):
    organization = db.query(Organization).filter(Organization.organization_id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return organization

@router.post("/")
async def create_organization(user: user_dependency, db: db_dependency, organization: CreateOrganizationRequest):
    existing_organization = (db.query(Organization).
                             filter(Organization.organization_name == organization.organization_name).first())
    if existing_organization:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Organization with this name already exists")
    new_organization = Organization(organization_name=organization.organization_name)
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    user_id = user["user_id"]
    owner_user = OrganizationUser(
        organization_id=new_organization.organization_id,
        user_id=user_id,
        role=UserRoleEnum.owner
    )
    db.add(owner_user)
    db.commit()
    return {"message": f"Organization {organization.organization_name} created successfully",}

@router.delete("/{organization_id}")
async def delete_organization(organization_id: int, db: db_dependency):
    organization = db.query(Organization).filter(Organization.organization_id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    db.query(OrganizationUser).filter(OrganizationUser.organization_id == organization_id).delete()

    db.delete(organization)
    db.commit()
    return {"message": f"Organization {organization.organization_name} deleted successfully"}

# TODO - Implement authorization checks for update and delete operations

@router.put("/{organization_id}")
async def update_organization(db: db_dependency, organization_id: int, organization: UpdateOrganizationRequest):
    existing_organization = db.query(Organization).filter(Organization.organization_id == organization_id).first()
    if not existing_organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    if organization.organization_name:
        existing_organization.organization_name = organization.organization_name
    existing_organization.updated_at = datetime.now(UTC)

    db.commit()
    db.refresh(existing_organization)
    return {"message": f"Organization {existing_organization.organization_name} updated successfully"}

