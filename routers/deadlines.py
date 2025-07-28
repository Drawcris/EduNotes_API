from fastapi import APIRouter, Depends, HTTPException, Form
from models.deadline import Deadline, EventTypeEnum
from models.organization_user import OrganizationUser
from models.user import User
from database import db_dependency
from services.auth_serivce import user_dependency
from schemas.deadline import ReadDeadline, CreateDeadline, UpdateDeadline

router = APIRouter(
    prefix="/deadlines",
    tags=["deadlines"],
    responses={404: {"description": "Not found"}}
)

@router.get("/my_deadlines", response_model=list[ReadDeadline])
async def get_my_deadlines(user: user_dependency, db: db_dependency):
    org_user = db.query(OrganizationUser).filter(OrganizationUser.user_id == user["user_id"]).all()
    if not org_user:
        raise HTTPException(status_code=404, detail="User not part of any organization")
    org_ids = [ou.organization_id for ou in org_user]
    deadlines = db.query(Deadline).filter(Deadline.organization_id.in_(org_ids)).all()
    if not deadlines:
        raise HTTPException(status_code=404, detail="User has no deadlines in their organization")
    return [deadline for deadline in deadlines]

#CRUD
@router.get("/", response_model=list[ReadDeadline])
async def read_deadlines(db: db_dependency):
    deadlines = db.query(Deadline).all()
    if not deadlines:
        raise HTTPException(status_code=404, detail="No deadlines found")
    return [deadline for deadline in deadlines]

@router.get("/{deadline_id}", response_model=ReadDeadline)
async def read_deadline(deadline_id: int, db: db_dependency):
    deadline = db.query(Deadline).filter(Deadline.deadline_id == deadline_id).first()
    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")
    return deadline

@router.post("/")
async def create_deadline(user: user_dependency,db: db_dependency, deadline: CreateDeadline = Form(...)):
    new_deadline = Deadline(
        event_type=deadline.event_type,
        event_name=deadline.event_name,
        event_description=deadline.event_description,
        event_date=deadline.event_date,
        organization_id=deadline.organization_id,
        created_by=user["user_id"]
    )
    db.add(new_deadline)
    db.commit()
    db.refresh(new_deadline)
    return new_deadline

@router.put("/{deadline_id}")
async def update_deadline(deadline_id: int, db: db_dependency, deadline: UpdateDeadline = Form(...)):
    existing_deadline = db.query(Deadline).filter(Deadline.deadline_id == deadline_id).first()
    if not existing_deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")

    existing_deadline.event_type = deadline.event_type
    existing_deadline.event_name = deadline.event_name
    existing_deadline.event_description = deadline.event_description
    existing_deadline.event_date = deadline.event_date

    db.commit()
    db.refresh(existing_deadline)
    return existing_deadline

@router.delete("/{deadline_id}")
async def delete_deadline(deadline_id: int, db: db_dependency):
    deadline = db.query(Deadline).filter(Deadline.deadline_id == deadline_id).first()
    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")

    db.delete(deadline)
    db.commit()
    return {"detail": "Deadline deleted successfully"}