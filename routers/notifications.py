from fastapi import APIRouter, Depends, HTTPException, status
from services.auth_serivce import user_dependency
from database import db_dependency
from models.notifications import Notification, NotificationStatusEnum
from schemas.notifications import ReadNotifications


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)

@router.get("/my", response_model=list[ReadNotifications])
async def get_my_notifications(user: user_dependency, db: db_dependency):
    notifications = db.query(Notification).filter(Notification.user_id == user["user_id"]).all()
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found for this user")
    return [notification for notification in notifications]

@router.put('/{notification_id}/read', response_model=ReadNotifications)
async def mark_notification_as_read(notification_id: int, user: user_dependency, db: db_dependency):
    notification = db.query(Notification).filter(
        Notification.notification_id == notification_id,
        Notification.user_id == user["user_id"]
    ).first()

    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    notification.status = NotificationStatusEnum.read
    db.commit()
    db.refresh(notification)
    return notification

@router.delete("/{notification_id}")
async def delete_my_notification(notification_id: int, user: user_dependency, db: db_dependency):
    notification = db.query(Notification).filter(
        Notification.notification_id == notification_id,
        Notification.user_id == user["user_id"]
    ).first()

    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}

@router.delete("/")
async def delete_all_my_notifications(user: user_dependency, db: db_dependency):
    notifications = db.query(Notification).filter(Notification.user_id == user["user_id"]).all()
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found for this user")

    for notification in notifications:
        db.delete(notification)
    db.commit()
    return {"message": "All notifications deleted successfully"}


# CRUD
@router.get("/", response_model=list[ReadNotifications])
async def get_notifications(db: db_dependency):
    notifications = db.query(Notification).all()
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")
    return [notification for notification in notifications]

@router.get("/{notification_id}", response_model=ReadNotifications)
async def get_notification(notification_id: int, db: db_dependency):
    notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification

