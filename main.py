from fastapi import FastAPI, Depends
from routes import auth, users, organizations
from sqlalchemy.orm import Session
from typing import Annotated
from routes.auth import get_current_user
from database import get_db


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organizations.router)


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
            ]
        },
        "organizations": {
            "description": "Organization management routes",
            "methods": ["GET", "POST", "DELETE", "PUT"],
            "endpoints": [
                "/organizations/",
                "/organizations/{organization_id}"
            ]
        }
    }
    return routes

