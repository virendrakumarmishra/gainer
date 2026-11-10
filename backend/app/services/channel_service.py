from app.repositories.channel_repository import ChannelRepository
from app.core.security import Security
from app.schemas.channel import ChannelRequest
from app.models.user import User
from app.models.channel import Channel
from fastapi import UploadFile


class ChannelService():
    def __init__(
        self,
        channel_repository: ChannelRepository,
        security: Security,
    ):
        self.user_repository = channel_repository
        self.security = security

    def store(self, payload: ChannelRequest, logo: UploadFile | None, user: User):
        logo_path = None

        if logo:
            # logo_path = self.save_logo(logo)
            pass

        channel = Channel(
            name=payload.name,
            handler=payload.handler,
            handler_link=str(payload.handler_link),
            logo_path=logo_path,
            user=user,
            status = payload.status
        )
        return self.channel_repository.create(channel)


    