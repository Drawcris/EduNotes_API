import enum

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship

class NotificationStatusEnum(str, enum.Enum):
    unread = "unread"
    read = "read"

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    message = Column(String, nullable=False)
    status = Column(Enum(NotificationStatusEnum), default=NotificationStatusEnum.unread)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="notifications")
