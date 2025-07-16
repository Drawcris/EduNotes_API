from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Organizations(Base):
    __tablename__ = "organizations"

    # TODO

class Channels(Base):
    __tablename__ = "channels"

    # TODO

class Topics(Base):
    __tablename__ = "topics"

    # TODO

class Notes(Base):
    __tablename__ = "notes"

    # TODO

class Users(Base):
    __tablename__ = "users"

    # TODO

class OrganizationUsers(Base):
    __tablename__ = "organization_users"

    # TODO