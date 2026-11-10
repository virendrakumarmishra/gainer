from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class EnvironmentType(str, Enum):
    LOCAL = "local"
    STG   = "staging"
    PROD  = "prod"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Gain Sub"
    SESSION_COOKIE_KEY: str = "session_id"
    SESSION_MAX_AGE: int = 120

    # Environment variable with default fallback to "local"
    ENVIRONMENT: EnvironmentType = EnvironmentType.LOCAL

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/course_platform_db"

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding= "utf-8",
        extra= "ignore"
    )

    @property
    def is_local(self):
        return self.ENVIRONMENT == EnvironmentType.LOCAL

    @property
    def is_prod(self):
        return self.ENVIRONMENT == EnvironmentType.PROD

    @property
    def is_stg(self):
        return self.ENVIRONMENT == EnvironmentType.STG

settings = Settings()
