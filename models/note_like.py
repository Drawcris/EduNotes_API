from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum

class LikeTypeEnum(str, enum.Enum):
    like = "like"
    dislike = "dislike"

class NoteLike(Base):
    __tablename__ = "note_likes"
    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("notes.note_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    type = Column(Enum(LikeTypeEnum), nullable=False)

    note = relationship("Note", back_populates="note_likes")
    __table_args__ = (UniqueConstraint("note_id", "user_id", name="unique_note_user_like"),)