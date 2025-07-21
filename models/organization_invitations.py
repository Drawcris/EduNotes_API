from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship
import enum


class StatusEnum(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"

class InvitedUserRoleEnum(str, enum.Enum):
    user = "user"
    owner = "owner"

class OrganizationInvitation(Base):
    __tablename__ = "organization_invitations"

    invitation_id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    role = Column(Enum(InvitedUserRoleEnum), default=InvitedUserRoleEnum.user, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    invited_by_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    organization = relationship("Organization", back_populates="invitations")
    invited_by_user = relationship("User", back_populates="invitations_sent")



