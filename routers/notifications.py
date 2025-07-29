from fastapi import APIRouter, Depends, HTTPException, status
from services.auth_serivce import user_dependency
from database import db_dependency
from models.notifications import Notification, NotificationStatusEnum
from schemas.notifications import ReadNotifications
from schemas.responses import StandardResponse


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)

@router.get("/my", response_model=StandardResponse[list[ReadNotifications]])
async def get_my_notifications(user: user_dependency, db: db_dependency):
    notifications = db.query(Notification).filter(Notification.user_id == user["user_id"]).all()
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found for this user")
    return StandardResponse(
        success=True,
        message="Notifications retrieved successfully",
        data=notifications
    )

@router.put('/{notification_id}/read', response_model=StandardResponse[ReadNotifications])
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
    return StandardResponse(
        success=True,
        message="Notification marked as read successfully",
        data=notification
    )

@router.delete("/{notification_id}", response_model=StandardResponse[ReadNotifications])
async def delete_my_notification(notification_id: int, user: user_dependency, db: db_dependency):
    notification = db.query(Notification).filter(
        Notification.notification_id == notification_id,
        Notification.user_id == user["user_id"]
    ).first()

    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return StandardResponse(
        success=True,
        message="Notification deleted successfully",
        data=notification
    )

@router.delete("/", response_model=StandardResponse[list[ReadNotifications]])
async def delete_all_my_notifications(user: user_dependency, db: db_dependency):
    notifications = db.query(Notification).filter(Notification.user_id == user["user_id"]).all()
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found for this user")

    for notification in notifications:
        db.delete(notification)
    db.commit()
    return StandardResponse(
        success=True,
        message="All notifications deleted successfully",
        data=notifications
    )


# CRUD
@router.get("/", response_model=StandardResponse[list[ReadNotifications]])
async def get_notifications(db: db_dependency):
    notifications = db.query(Notification).all()
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")
    return StandardResponse(
        success=True,
        message="Notifications retrieved successfully",
        data=notifications
    )

@router.get("/{notification_id}", response_model=StandardResponse[ReadNotifications])
async def get_notification(notification_id: int, db: db_dependency):
    notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return StandardResponse(
        success=True,
        message="Notification retrieved successfully",
        data=notification
    )

