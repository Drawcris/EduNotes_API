from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship

class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="channels")
    topics = relationship("Topic", back_populates="channel")