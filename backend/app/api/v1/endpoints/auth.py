from fastapi import APIRouter, Depends, Request, Response, status

from app.api.deps import get_auth_service, get_current_user
from app.core.config import settings
from app.models.user import User
from app.schemas.user import (
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    payload: UserRegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.register_user(payload)


@router.post(
    "/login",
    summary="Login and obtain HttpOnly session cookie",
)
def login(
    payload: UserLoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    user, session_id, max_age = auth_service.authenticate_user(payload)

    response.set_cookie(
        key=settings.SESSION_COOKIE_KEY,
        value=session_id,
        httponly=True,
        max_age=max_age,
        samesite="lax",
        secure=settings.is_prod,
        path="/",
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }


@router.post(
    "/logout",
    summary="Logout user and invalidate session",
)
def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    session_id = request.cookies.get(settings.SESSION_COOKIE_KEY)
    auth_service.logout_user(session_id)

    response.delete_cookie(
        key=settings.SESSION_COOKIE_KEY,
        path="/",
    )

    return {"message": "Logged out successfully"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get currently authenticated user",
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user