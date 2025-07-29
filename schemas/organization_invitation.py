from datetime import datetime
from pydantic import BaseModel
from models.organization_invitations import InvitedUserRoleEnum, StatusEnum

class ReadOrganizationInvitation(BaseModel):
    invitation_id: int
    organization_id: int
    email: str
    role: InvitedUserRoleEnum
    status: StatusEnum
    invited_by_user_id: int
    created_at: datetime