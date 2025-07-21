from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from routers import (auth, users, organizations, channels, topics, notes, organization_user, organization_invitations,
                     ranking)
from sqlalchemy.orm import Session
from typing import Annotated
from database import get_db


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organizations.router)
app.include_router(channels.router)
app.include_router(topics.router)
app.include_router(notes.router)
app.include_router(organization_user.router)
app.include_router(organization_invitations.router)
app.include_router(ranking.router)

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
def read_root():
    routes = {
        "auth": {
            "description": "Authentication routers",
            "methods": ["POST"],
            "endpoints": [
                "/auth/login",
                "/auth/register"
            ]
        },
        "users": {
            "description": "User management routers",
            "methods": ["GET", "DELETE", "PUT"],
            "endpoints": [
                "/users/",
                "/users/{user_id}"
                "/users/{user_id}/avatar",
                "/users/{user_id}/increase_score",
                "/users/{user_id}/decrease_score"
            ]
        },
        "organizations": {
            "description": "Organization management routers",
            "methods": ["GET", "POST", "DELETE", "PUT"],
            "endpoints": [
                "/organizations/",
                "/organizations/{organization_id}"
            ]
        },
        "channels": {
            "description": "Channel management routers",
            "methods": ["GET", "POST", "DELETE", "PUT"],
            "endpoints": [
                "/channels/",
                "/channels/{channel_id}",
                "/channels/channels_in_organization"
            ]
        },
        "topics": {
            "description": "Topic management routers",
            "methods": ["GET", "POST", "DELETE", "PUT"],
            "endpoints": [
                "/topics/",
                "/topics/{topic_id}",
                "/topics/topics_in_channel"
            ]
        },
        "notes": {
            "description": "Note management routers",
            "methods": ["GET", "POST", "DELETE"],
            "endpoints": [
                "/notes/",
                "/notes/{note_id}",
                "/notes/notes_in_topic"
            ]
        },
        "organization_user": {
            "description": "Organization user management routers",
            "methods": ["POST", "DELETE", "GET", "PUT"],
            "endpoints": [
                "/organization_user/",
                "/organization_user/me",
                "/organization_user/{organization_user_id}",
                "/organization_user/{organization_user_id}/role",
                "/organization_user/invite",
                "/organization_user/RemoveUserFromOrganization",
            ]
        }

    }
    return routes

