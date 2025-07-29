from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from models.note import Note, NoteContentTypeEnum
from models.user import User
from models.note_like import NoteLike, LikeTypeEnum
from database import db_dependency
from schemas.note import ReadNoteResponse
from schemas.responses import StandardResponse
from services.rank_service import get_rank_for_score
from uuid import uuid4
from services.auth_serivce import user_dependency
import os


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)
@router.get("/my", response_model=StandardResponse[list[ReadNoteResponse]])
async def read_my_notes(user: user_dependency, db: db_dependency):
    notes = db.query(Note).filter(Note.user_id == user["user_id"]).all()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found for this user")
    return StandardResponse(
        success=True,
        message="Your notes retrieved successfully",
        data=notes
    )
@router.get("/notes_in_topic", response_model=StandardResponse[list[ReadNoteResponse]])
async def read_notes_in_topic(topic_id: int, db: db_dependency):
    notes = db.query(Note).filter(Note.topic_id == topic_id).all()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found in this topic")
    return StandardResponse(
        success=True,
        message="Notes retrieved successfully",
        data=notes
    )

@router.post("/give_like", response_model=StandardResponse[dict])
async def give_like(note_id: int, user: user_dependency, db: db_dependency):
    existing = db.query(NoteLike).filter_by(note_id=note_id, user_id=user["user_id"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already like/disliked this note")
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note does not exist")
    note.likes += 1
    db.add(NoteLike(note_id=note_id, user_id=user["user_id"], type=LikeTypeEnum.like))
    db.commit()
    db.refresh(note)
    author = db.query(User).filter(User.user_id == note.user_id).first()
    author.score += 1
    author.rank = get_rank_for_score(author.score)
    db.commit()
    db.refresh(author)
    return StandardResponse(
        success=True,
        message=f"Note has been liked",
        data={"likes": note.likes, "author_score": author.score,
              "author_rank": author.rank, "author_id": author.user_id,
              "note_id": note.note_id}
    )

@router.post("/give_dislike", response_model=StandardResponse[dict])
async def give_dislike(note_id: int, user: user_dependency, db: db_dependency):
    existing = db.query(NoteLike).filter_by(note_id=note_id, user_id=user["user_id"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already like/disliked this note")
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note does not exist")
    note.likes -= 1
    db.add(NoteLike(note_id=note_id, user_id=user["user_id"], type=LikeTypeEnum.dislike))
    db.commit()
    db.refresh(note)
    author = db.query(User).filter(User.user_id == note.user_id).first()
    author.score -= 1
    author.rank = get_rank_for_score(author.score)
    db.commit()
    db.refresh(author)
    return StandardResponse(
        success=True,
        message=f"Note has been disliked",
        data={"likes": note.likes, "author_score": author.score,
              "author_rank": author.rank, "author_id": author.user_id,
              "note_id": note.note_id}
    )
# CRUD

@router.get("/", response_model=StandardResponse[list[ReadNoteResponse]])
async def read_notes(db: db_dependency):
    notes = db.query(Note).all()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found")
    return StandardResponse(
        success=True,
        message="Notes retrieved successfully",
        data=notes
    )

@router.get("/{note_id}", response_model=StandardResponse[ReadNoteResponse])
async def read_note(db: db_dependency, note_id: int):
    note = db.query(Note).filter_by(note_id=note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found")
    return StandardResponse(
        success=True,
        message="Note retrieved successfully",
        data=note
    )

@router.post("/", response_model=StandardResponse[ReadNoteResponse])
async def create_note(
    user: user_dependency,
    title: str = Form(...),
    topic_id: int = Form(...),
    organization_id: int = Form(...),
    content_type: NoteContentTypeEnum = Form(...),
    content: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: db_dependency = None
):
    image_url = None
    if content_type == "image" and image:
        filename = f"{uuid4()}_{image.filename}"
        file_path = os.path.join("media", "note_imgs", filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        image_url = f"/media/note_imgs/{filename}"
        content = None
    elif content_type == "text":
        image_url = None

    new_note = Note(
        title=title,
        topic_id=topic_id,
        organization_id=organization_id,
        user_id=user["user_id"],
        content_type=content_type,
        content=content,
        image_url=image_url
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return StandardResponse(
        success=True,
        message="Note created successfully",
        data=new_note
    )

@router.delete("/{note_id}", response_model=StandardResponse[ReadNoteResponse])
async def delete_note(db: db_dependency, note_id: int):
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    db.delete(note)
    db.commit()
    return StandardResponse(
        success=True,
        message="Note deleted successfully",
        data=None
    )