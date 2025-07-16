from dotenv import load_dotenv
import os

from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# TODO