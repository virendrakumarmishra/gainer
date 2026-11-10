from sqlalchemy.orm import Session
from app.models.channel import Channel

class ChannelRepository():
    def __init__(self, db: Session):
        pass

    def create(self, channel: Channel):
        self.db.add(channel)
        self.db.commit()
        self.db.refresh(channel)
        return channel