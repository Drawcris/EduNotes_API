from fastapi import APIRouter, HTTPException, status
from database import db_dependency
from models import Channel, Organization
from schemas import ReadChannelResponse, CreateChannelRequest, UpdateChannelRequest

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
)

@router.get("/", response_model=list[ReadChannelResponse])
async def read_channels(db: db_dependency):
    channels = db.query(Channel).all()
    if not channels:
        raise HTTPException(status_code=404, detail="Channels not found")
    return [channel for channel in channels]

@router.get("/{channel_id}", response_model=ReadChannelResponse)
async def read_channel(channel_id: int, db: db_dependency):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.post("/")
async def create_channel(channel: CreateChannelRequest, db: db_dependency):
    existing_channel = db.query(Channel).filter(Channel.channel_name == channel.channel_name).first()
    if existing_channel:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Channel with this name already exists")
    chosen_organization = channel.organization_id
    if not db.query(Organization).filter(Organization.organization_id == chosen_organization).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    new_channel = Channel(
        channel_name=channel.channel_name,
        organization_id=channel.organization_id
    )
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return {"message": f"Channel {channel.channel_name} created successfully"}

@router.delete("/{channel_id}")
async def delete_channel(channel_id: int, db: db_dependency):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    db.delete(channel)
    db.commit()
    return {"message": f"Channel {channel.channel_name} deleted successfully"}

@router.put("/{channel_id}")
async def update_channel(channel_id: int, channel: CreateChannelRequest, db: db_dependency):
    existing_channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not existing_channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    if channel.channel_name:
        existing_channel.channel_name = channel.channel_name
    if channel.organization_id:
        if not db.query(Organization).filter(Organization.organization_id == channel.organization_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        existing_channel.organization_id = channel.organization_id

    db.commit()
    return {"message": f"Channel {existing_channel.channel_name} updated successfully"}

@router.put("/{channel_id}/")
async def update_channel_name(channel_id: int, channel: UpdateChannelRequest, db: db_dependency):
    existing_channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    old_name = existing_channel.channel_name
    if not existing_channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    if channel.channel_name:
        existing_channel.channel_name = channel.channel_name

    db.commit()
    db.refresh(existing_channel)
    return {"message": f"Channel {old_name} updated to {existing_channel.channel_name} successfully"}

