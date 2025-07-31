from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import (auth, users, organizations, channels, topics, notes, organization_user, organization_invitations,
                     ranking, notifications, deadlines, ai_summary)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organizations.router)
app.include_router(channels.router)
app.include_router(topics.router)
app.include_router(notes.router)
app.include_router(organization_user.router)
app.include_router(organization_invitations.router)
app.include_router(ranking.router)
app.include_router(deadlines.router)
app.include_router(notifications.router)
app.include_router(ai_summary.router)

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
def read_root():
    return {
        "name": "EduNotes API",
        "version": "1.0.0",
        "description": "API for managing study notes, organizations and collaborative learning with AI features.",
        "endpoints": {
            "auth": {
                "login": "/auth/login",
                "register": "/auth/register"
            },
            "users": "/users",
            "organizations": "/organizations",
            "organization_user": "/organization_user",
            "organization_invitations": "/organization_invitations",
            "channels": "/channels",
            "topics": "/topics",
            "notes": "/notes",
            "features": {
                "ranking": "/ranking",
                "deadlines": "/deadlines",
                "notifications": "/notifications",
                "ai_summary": "/ai_summary"
            }
        },
        "documentation": "/docs",
        "openapi": "/openapi.json",
        "media_files": "/media",
        "status": "active",
    }

