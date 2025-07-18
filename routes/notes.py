from fastapi import APIRouter, HTTPException, status
from models import Note
from database import db_dependency


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

@router.get("/")
def read_placeholder():
    return {"message": "This is a placeholder for the notes API."}