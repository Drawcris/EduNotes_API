from models.user import User
from schemas.responses import StandardResponse
from fastapi import APIRouter, HTTPException, status
from database import db_dependency
from services.auth_serivce import user_dependency
from services.rank_service import get_rank_for_score

router = APIRouter(
    prefix="/ranking",
    tags=["ranking"],
)
@router.get("/my", response_model=StandardResponse[dict])
async def get_my_score(user: user_dependency, db: db_dependency):
    user = db.query(User).filter(User.user_id == user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return StandardResponse(
        success=True,
        message="User score retrieved successfully",
        data={"username": user.username, "score": user.score, "rank": user.rank.value}
    )

@router.get("/", response_model=StandardResponse[list[dict]])
async def get_all_users_score(db: db_dependency):
    users = db.query(User).order_by(User.score.desc()).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return StandardResponse(
        success=True,
        message="All users scores retrieved successfully",
        data=[{"username": user.username, "score": user.score, "rank": user.rank.value} for user in users]
    )

@router.get("/{user_id}", response_model=StandardResponse[dict])
async def get_user_score(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return StandardResponse(
        success=True,
        message="User score retrieved successfully",
        data={"username": user.username, "score": user.score, "rank": user.rank.value}
    )

