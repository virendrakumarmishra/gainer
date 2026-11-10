from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.core.logger import logger

from app.core.config import settings
from app.core.security import Security
from app.models.session import UserSession
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLoginRequest, UserRegisterRequest


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session_repo: SessionRepository,
        security: Security,
    ):
        self.user_repository = user_repository
        self.session_repo = session_repo
        self.security = security

    def register_user(self, payload: UserRegisterRequest) -> User:
        # 1. Duplicate email check
        existing_user = self.user_repository.get_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        # 2. Hash password with Argon2
        hashed_password = self.security.hash_password(payload.password)
        

        # 3. Model create & save
        new_user = User(
            name=payload.name,
            email=payload.email,
            password=hashed_password,
            role=payload.role,
        )

        return self.user_repository.create(new_user)

    def authenticate_user(self, payload: UserLoginRequest) -> tuple[User, str, int]:
        # 1. Check user credentials
        user = self.user_repository.get_by_email(payload.email)
        if not user or not self.security.verify_password(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # 2. Generate secure session ID
        session_id = self.security.generate_session_id()
        max_age = settings.SESSION_MAX_AGE
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=max_age)

        # 3. Save session in database
        new_session = UserSession(
            session_id=session_id,
            user_id=user.id,
            expires_at=expires_at,
        )
        self.session_repo.create(new_session)

        return user, session_id, max_age

    def logout_user(self, session_id: str | None) -> None:
        if session_id:
            self.session_repo.delete_by_session_id(session_id)