from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import Security
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.repositories.channel_repository import ChannelRepository
from app.services.channel_service import ChannelService


def get_security_service() -> Security:
    return Security()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_session_repository(db: Session = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    session_repo: SessionRepository = Depends(get_session_repository),
    security: Security = Depends(get_security_service),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        session_repo=session_repo,
        security=security,
    )


def get_current_user(
    request: Request,
    session_repo: SessionRepository = Depends(get_session_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    # Settings se cookie key uthayenge
    session_id = request.cookies.get(settings.SESSION_COOKIE_KEY)
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    # Valid session check
    user_session = session_repo.get_valid_session(session_id)
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired or is invalid.",
        )

    # User fetch
    user = user_repository.get_by_id(user_session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user


def get_channel_repository(db: Session = Depends(get_db)) -> ChannelRepository:
    return ChannelRepository(db)


def get_channel_service(
    channel_repo: ChannelRepository = Depends(get_channel_repository),
) -> ChannelService:
    return ChannelService(channel_repo=channel_repo)