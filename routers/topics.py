from fastapi import APIRouter, HTTPException, status
from models.topic import Topic
from models.organization import Organization
from models.channel import Channel
from database import db_dependency
from schemas.topic import ReadTopicResponse, CreateTopicRequest, UpdateTopicRequest
from datetime import datetime, UTC

router = APIRouter(
    prefix="/topics",
    tags=["topics"],
)

@router.get("/topics_in_channel")
async def read_topics_in_channel(channel_id: int, db: db_dependency):
    topics = db.query(Topic).filter(Topic.channel_id == channel_id).all()
    if not topics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No topics found in this channel")
    return [topic for topic in topics]

# CRUD

@router.get("/", response_model=list[ReadTopicResponse])
async def read_topics(db: db_dependency):
    topics = db.query(Topic).all()
    if not topics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No topics found")
    return [topic for topic in topics]

@router.get("/{topic_id}", response_model=ReadTopicResponse)
async def read_topic(db: db_dependency, topic_id: int):
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No topic found")
    return topic

@router.post("/")
async def create_topic(topic: CreateTopicRequest, db: db_dependency):
    existing_topic = db.query(Topic).filter(Topic.topic_name == topic.topic_name).first()
    if existing_topic:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic with this name already exists")
    existing_organization = db.query(Organization).filter(Organization.organization_id == topic.organization_id).first()
    if not existing_organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    chosen_channel = topic.channel_id
    if not db.query(Channel).filter(Channel.channel_id == chosen_channel).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

    new_topic = Topic(
        topic_name=topic.topic_name,
        channel_id=topic.channel_id,
        organization_id=topic.organization_id
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return {"message": f"Topic {topic.topic_name} created successfully"}

@router.delete("/{topic_id}")
async def delete_topic(topic_id: int, db: db_dependency):
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    db.delete(topic)
    db.commit()
    return {"message": f"Topic {topic.topic_name} deleted successfully"}

@router.put("/{topic_id}")
async def update_topic(db: db_dependency, topic_id: int, topic: UpdateTopicRequest):
    existing_topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()
    if not existing_topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

    if topic.topic_name:
        existing_topic.topic_name = topic.topic_name
    if topic.channel_id:
        existing_topic.channel_id = topic.channel_id
    if topic.organization_id:
        existing_topic.organization_id = topic.organization_id
    existing_topic.updated_at = datetime.now(UTC)

    db.commit()
    db.refresh(existing_topic)
    return {"message": f"Topic {existing_topic.topic_name} updated successfully"}
