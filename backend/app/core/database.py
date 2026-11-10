from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


class DatabaseSessionManager:
    def __init__(self, db_url: str, echo: bool = False):
        # 1. Connection Pool & Engine initialization
        self._engine = create_engine(
            db_url,
            echo=echo,
            pool_pre_ping=True,      # Stale connections detect then reconnect
            pool_size=10,            # Normal pool limit
            max_overflow=20,         # Peak load par extra connections
        )
        
        # 2. Session Factory
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_session(self) -> Generator[Session, None, None]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def close(self):
        if self._engine:
            self._engine.dispose()


# Singleton Instance
db_manager = DatabaseSessionManager(
    db_url=settings.DATABASE_URL,
    echo=settings.is_local
)


# FastAPI Dependency inject in routes/repositories
def get_db() -> Generator[Session, None, None]:
    yield from db_manager.get_session()