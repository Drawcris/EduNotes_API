from fastapi import APIRouter, Depends, HTTPException, status
from services.auth_serivce import user_dependency
from models.organization_invitations import OrganizationInvitation, StatusEnum
from models.organization_user import OrganizationUser
from database import db_dependency
from models.organization_user import UserRoleEnum
from models.user import User

router = APIRouter(
    prefix="/organization-invitations",
    tags=["Organization Invitations"],
)

@router.post("/")
async def invite_user(organization_id: int, email: str, role: UserRoleEnum, user: user_dependency, db: db_dependency):
    org_user = db.query(OrganizationUser).filter_by(
        organization_id=organization_id,
        user_id=user["user_id"],
        role=UserRoleEnum.owner
    ).first()
    if not org_user:
        raise HTTPException(status_code=403, detail="No permission to invite users to this organization")

    invited_user = db.query(User).filter_by(email=email).first()
    if not invited_user:
        raise HTTPException(status_code=404, detail="User with this email does not exist")

    already_in_org = db.query(OrganizationUser).filter_by(
        organization_id=organization_id,
        user_id=invited_user.user_id
    ).first()
    if already_in_org:
        raise HTTPException(status_code=400, detail="User is already a member of this organization")

    invitation = OrganizationInvitation(
        organization_id=organization_id,
        email=email,
        role=role,
        invited_by_user_id=user["user_id"]
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return {"message": "Invitation sent successfully"}

@router.post("/{invitation_id}/decline")
async def decline_invitation(invitation_id: int, user: user_dependency, db: db_dependency):
    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.invitation_id == invitation_id,
        OrganizationInvitation.email == user["email"]
    ).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    invitation.status = StatusEnum.declined
    db.commit()
    return {"message": "Invitation declined"}

@router.get("/my")
async def my_invitations(user: user_dependency, db: db_dependency):
    invitations = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.email == user["email"]
    ).all()
    if not invitations:
        raise HTTPException(status_code=404, detail="No invitations found")
    return invitations

@router.get("/sent")
async def sent_invitations(user: user_dependency, db: db_dependency):
    invitations = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.invited_by_user_id == user["user_id"]
    ).all()
    if not invitations:
        raise HTTPException(status_code=404, detail="No sent invitations found")
    return invitations