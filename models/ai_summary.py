from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class AI_Summary(Base):
    __tablename__ = "ai_summary"

    summary_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.topic_id"), nullable=False)
    summary_text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    topic = relationship("Topic", back_populates="ai_summaries")