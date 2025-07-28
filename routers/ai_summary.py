from fastapi import APIRouter, Depends, HTTPException, Query
from services.AI_services import summarize_notes_with_deepseek
from database import db_dependency
from models.ai_summary import AI_Summary
from schemas.ai_summary import ReadAISummary

router = APIRouter(
    prefix="/ai_summary",
    tags=["AI Summary"],
)

@router.get("/", response_model=list[ReadAISummary])
async def get_ai_summary(db: db_dependency):
    summaries = db.query(AI_Summary).all()
    if not summaries:
        raise HTTPException(status_code=404, detail="No AI summaries found")
    return [summary for summary in summaries]

@router.post("/")
async def create_ai_summary(db: db_dependency, topic_id: int):
    summary_text = summarize_notes_with_deepseek(topic_id, db)
    if not summary_text:
        raise HTTPException(status_code=400, detail="Failed to generate summary")

    new_summary = AI_Summary(topic_id=topic_id, summary_text=summary_text)
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    return new_summary

@router.put("/{summary_id}")
async def update_ai_summary(summary_id: int, topic_id: int, db: db_dependency):
    summary = db.query(AI_Summary).filter(AI_Summary.summary_id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="AI Summary not found")

    summary_text = summarize_notes_with_deepseek(topic_id, db)
    if not summary_text:
        raise HTTPException(status_code=400, detail="Failed to generate summary")

    summary.topic_id = topic_id
    summary.summary_text = summary_text
    db.commit()
    db.refresh(summary)

    return {"message": "AI Summary updated successfully", "summary": summary}
@router.delete("/{summary_id}")
async def delete_ai_summary(summary_id: int, db: db_dependency):
    summary = db.query(AI_Summary).filter(AI_Summary.summary_id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="AI Summary not found")

    db.delete(summary)
    db.commit()

    return {"detail": "AI Summary deleted successfully"}