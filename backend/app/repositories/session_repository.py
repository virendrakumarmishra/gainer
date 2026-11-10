from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from app.models.session import UserSession


class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, session: UserSession) -> UserSession:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_valid_session(self, session_id: str) -> Optional[UserSession]:
        
        now = datetime.now(timezone.utc)
        return (
            self.db.query(UserSession)
            .filter(
                UserSession.session_id == session_id,
                UserSession.expires_at > now,
            )
            .first()
        )

    def delete_by_session_id(self, session_id: str) -> None:
        
        self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).delete(synchronize_session=False)
        self.db.commit()

    def delete_all_for_user(self, user_id: int) -> None:
        self.db.query(UserSession).filter(
            UserSession.user_id == user_id
        ).delete(synchronize_session=False)
        self.db.commit()