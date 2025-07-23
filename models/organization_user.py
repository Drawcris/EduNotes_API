from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship
import enum

class UserRoleEnum(str, enum.Enum):
    owner = "owner"
    user = "user"


class OrganizationUser(Base):
    __tablename__ = "organization_users"

    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.user)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="users")
    user = relationship("User", back_populates="organizations")