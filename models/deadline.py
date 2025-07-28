from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
import enum

class EventTypeEnum(str, enum.Enum):
    exam = "Egzamin"
    assignment = "Zadanie"

class Deadline(Base):
    __tablename__ = "deadlines"

    deadline_id = Column(Integer, primary_key=True)
    event_type = Column(Enum(EventTypeEnum), nullable=False)
    event_name = Column(String, nullable=False)
    event_description = Column(String, nullable=True)
    event_date = Column(DateTime(timezone=True), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id", ondelete="CASCADE"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="deadlines")
    creator = relationship("User")


