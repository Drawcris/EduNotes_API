from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship
import enum

class NoteContentTypeEnum(str, enum.Enum):
    text = "text"
    image = "image"

class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content_type = Column(Enum(NoteContentTypeEnum), nullable=False)
    content = Column(Text, nullable=True)  # for text content
    image_url = Column(String, nullable=True)  # for images
    topic_id = Column(Integer, ForeignKey("topics.topic_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    likes = Column(Integer, default=0)  # Number of likes
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    topic = relationship("Topic", back_populates="notes")
    user = relationship("User", back_populates="notes")
    organization = relationship("Organization", back_populates="notes")
