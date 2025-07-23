from models.user import User

from fastapi import APIRouter, HTTPException, status
from database import db_dependency
from services.auth_serivce import user_dependency
from services.rank_service import get_rank_for_score

router = APIRouter(
    prefix="/ranking",
    tags=["ranking"],
)
@router.get("/my")
async def get_my_score(user: user_dependency, db: db_dependency):
    user = db.query(User).filter(User.user_id == user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"username": user.username,
              "score": user.score,
            "rank": user.rank.value,}

@router.get("/")
async def get_all_users_score(db: db_dependency):
    users = db.query(User).order_by(User.score.desc()).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return [{"username": user.username, "score": user.score} for user in users]

@router.get("/{user_id}")
async def get_user_score(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"username": user.username, "score": user.score}

@router.post("/{user_id}/increase_score")
async def increase_score(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.score += 1
    user.rank = get_rank_for_score(user.score)
    db.commit()
    db.refresh(user)
    return {"message": f"Score for user {user.username} increased successfully", "new_score": user.score,
            "current_rank": user.rank.value}

@router.post("/{user_id}/decrease_score")
async def decrease_score(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.score -= 1
    user.rank = get_rank_for_score(user.score)
    db.commit()
    db.refresh(user)
    return {"message": f"Score for user {user.username} decreased successfully", "new_score": user.score,
            "current_rank": user.rank.value}