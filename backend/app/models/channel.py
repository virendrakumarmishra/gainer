from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Enum as SQLEnum
from datetime import datetime, timezone
from app.enums.channel_status import ChannelStatus


class Channel(Base):
    __tablename__ = 'channels'

    #column names
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    handler: Mapped[str] = mapped_column(String(255), nullable=False)
    handler_link: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[ChannelStatus] = mapped_column(
        SQLEnum(ChannelStatus, name="channel_status"), 
        default=ChannelStatus.PENDING, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="channel"
    )