from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from routes import auth, users, organizations, channels, topics, notes, organization_user
from sqlalchemy.orm import Session
from typing import Annotated
from routes.auth import get_current_user
from database import get_db


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organizations.router)
app.include_router(channels.router)
app.include_router(topics.router)
app.include_router(notes.router)
app.include_router(organization_user.router)

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
def read_root():
    routes = {
        "auth": {
            "description": "Authentication routes",
            "methods": ["POST"],
            "endpoints": [
                "/auth/login",
                "/auth/register"
            ]
        },
        "users": {
            "description": "User management routes",
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
            "description": "Organization management routes",
            "methods": ["GET", "POST", "DELETE", "PUT"],
            "endpoints": [
                "/organizations/",
                "/organizations/{organization_id}"
            ]
        },
        "channels": {
            "description": "Channel management routes",
            "methods": ["GET", "POST", "DELETE", "PUT"],
            "endpoints": [
                "/channels/",
                "/channels/{channel_id}",
            ]
        },
        "topics": {
            "description": "Topic management routes",
            "methods": ["GET", "POST", "DELETE", "PUT"],
            "endpoints": [
                "/topics/",
                "/topics/{topic_id}",
            ]
        },
        "notes": {
            "description": "Note management routes",
            "methods": ["GET", "POST", "DELETE"],
            "endpoints": [
                "/notes/",
                "/notes/{note_id}",
            ]
        }

    }
    return routes

