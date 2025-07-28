from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship


class Topic(Base):
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True)
    topic_name = Column(String, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    channel = relationship("Channel", back_populates="topics")
    organization = relationship("Organization", back_populates="topics")
    notes = relationship("Note", back_populates="topic")
    ai_summaries = relationship("AI_Summary", back_populates="topic")