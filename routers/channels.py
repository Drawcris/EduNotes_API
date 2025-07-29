from fastapi import APIRouter, HTTPException, status
from database import db_dependency
from models.channel import Channel
from models.organization import Organization
from models.organization_user import OrganizationUser
from schemas.channel import ReadChannelResponse, CreateChannelRequest, UpdateChannelRequest
from schemas.responses import StandardResponse
from services.auth_serivce import user_dependency

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
)

@router.get("/channels_in_organization", response_model=StandardResponse[list[ReadChannelResponse]])
async def read_channels_in_organization(organization_id: int, db: db_dependency):
    channels = db.query(Channel).filter(Channel.organization_id == organization_id).all()
    if not channels:
        raise HTTPException(status_code=404, detail="No channels found in this organization")
    return StandardResponse(
        success=True,
        message="Your channels in this organization retrieved successfully",
        data=[channel for channel in channels]
    )


# CRUD

@router.get("/", response_model=StandardResponse[list[ReadChannelResponse]])
async def read_channels(db: db_dependency):
    channels = db.query(Channel).all()
    if not channels:
        raise HTTPException(status_code=404, detail="Channels not found")
    return StandardResponse(
        success=True,
        message="Channels retrieved successfully",
        data=[channel for channel in channels]
    )

@router.get("/{channel_id}", response_model=StandardResponse[ReadChannelResponse])
async def read_channel(channel_id: int, db: db_dependency):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return StandardResponse(
        success=True,
        message="Channel retrieved successfully",
        data=channel
    )

@router.post("/", response_model=StandardResponse[ReadChannelResponse])
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
    return StandardResponse(
        success=True,
        message=f"Channel created successfully",
        data=new_channel
    )


@router.delete("/{channel_id}", response_model=StandardResponse[ReadChannelResponse])
async def delete_channel(channel_id: int, db: db_dependency, user: user_dependency):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    org_user = db.query(OrganizationUser).filter(
        OrganizationUser.organization_id == channel.organization_id,
        OrganizationUser.user_id == user["user_id"],
        OrganizationUser.role == "owner"
    ).first()

    if not org_user:
        raise HTTPException(
            status_code=403,
            detail="Only organization owners can delete channels"
        )

    db.delete(channel)
    db.commit()
    return StandardResponse(
        success=True,
        message=f"Channel deleted successfully",
        data=channel
    )

@router.put("/{channel_id}", response_model=StandardResponse[ReadChannelResponse])
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
    return StandardResponse(
        success=True,
        message="Channel updated successfully",
        data=existing_channel
    )