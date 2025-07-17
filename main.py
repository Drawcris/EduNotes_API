from fastapi import FastAPI
from routes import auth, users
app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


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
            "methods": ["GET", "DELETE"],
            "endpoints": [
                "/users/",
                "/users/{user_id}"
            ]
        }
    }
    return routes