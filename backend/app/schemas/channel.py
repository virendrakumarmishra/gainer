from pydantic import BaseModel, HttpUrl
from app.enums.channel_status import ChannelStatus



class ChannelRequest(BaseModel):
    name: str
    handler: str
    handler_link: HttpUrl
    status: ChannelStatus = ChannelStatus.PENDING
    
