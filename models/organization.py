from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(Integer, primary_key=True)
    organization_name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    invitations = relationship("OrganizationInvitation", back_populates="organization")

    channels = relationship("Channel", back_populates="organization", passive_deletes=True)
    topics = relationship("Topic", back_populates="organization", passive_deletes=True)
    notes = relationship("Note", back_populates="organization", passive_deletes=True)
    users = relationship("OrganizationUser", back_populates="organization", passive_deletes=True)