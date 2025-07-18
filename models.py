from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship
import enum


class UserRoleEnum(str, enum.Enum):
    owner = "Owner"
    user = "user"

class NoteContentTypeEnum(str, enum.Enum):
    text = "text"
    image = "image"


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(Integer, primary_key=True)
    organization_name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    channels = relationship("Channel", back_populates="organization")
    topics = relationship("Topic", back_populates="organization")
    notes = relationship("Note", back_populates="organization")
    users = relationship("OrganizationUser", back_populates="organization")


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

    notes = relationship("Note", back_populates="user")
    organizations = relationship("OrganizationUser", back_populates="user")


class OrganizationUser(Base):
    __tablename__ = "organization_users"

    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.user)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="users")
    user = relationship("User", back_populates="organizations")


class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="channels")
    topics = relationship("Topic", back_populates="channel")


class Topic(Base):
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True)
    topic_name = Column(String, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    channel = relationship("Channel", back_populates="topics")
    organization = relationship("Organization", back_populates="topics")
    notes = relationship("Note", back_populates="topic")


class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content_type = Column(Enum(NoteContentTypeEnum), nullable=False)
    content = Column(Text, nullable=True)  # for text content
    image_url = Column(String, nullable=True)  # for images
    topic_id = Column(Integer, ForeignKey("topics.topic_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    topic = relationship("Topic", back_populates="notes")
    user = relationship("User", back_populates="notes")
    organization = relationship("Organization", back_populates="notes")
