from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from sqlalchemy.orm import relationship
from models.organization_invitations import OrganizationInvitation
from database import Base
import enum


class RankEnum(str, enum.Enum):
    incompetent = "niekompetentny"
    beginner = "początkujący"
    specialist = "specalista"
    expert = "ekspert"
    master = "mistrz"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    avatar_url = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    score = Column(Integer, default=0)
    invitations_sent = relationship("OrganizationInvitation", back_populates="invited_by_user")
    rank = Column(Enum(RankEnum), default=RankEnum.beginner)

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    note_likes = relationship("NoteLike", cascade="all, delete-orphan")
    organizations = relationship("OrganizationUser", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
