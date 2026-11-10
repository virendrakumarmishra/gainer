from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.enums.user_role import UserRole

class UserRegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="User full name")
    email: EmailStr
    password: str = Field(min_length=6, max_length=64, description="Plain text password")
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str