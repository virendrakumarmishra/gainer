from fastapi import APIRouter, File, Form, UploadFile, Depends, status

from app.schemas.channel import ChannelRequest
from app.models.user import User
from app.api.deps import get_current_user, get_channel_service
from app.services.channel_service import ChannelService

router = APIRouter()


@router.post(
    "/channels",
    status_code=status.HTTP_201_CREATED,
    summary="Add your YouTube channel details",
)
def store(
    name: str = Form(...),
    handler: str = Form(...),
    handler_link: str = Form(...),
    logo: UploadFile | None = File(default=None),
    current_user: User = Depends(get_current_user),
    channel_service: ChannelService = Depends(get_channel_service),
):
    payload = ChannelRequest(
        name=name,
        handler=handler,
        handler_link=handler_link,
    )

    return channel_service.store(
        payload=payload,
        logo=logo,
        user=current_user,
    )