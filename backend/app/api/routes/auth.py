from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user
from app.core.config import settings
from app.core.db import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, response_model_by_alias=True
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    if auth_service.get_user_by_email(db, payload.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="此 email 已被註冊")

    user = auth_service.create_user(
        db, email=payload.email, password=payload.password, display_name=payload.display_name
    )
    return UserResponse(id=user.id, email=user.email, display_name=user.display_name)


@router.post("/login", response_model=UserResponse, response_model_by_alias=True)
async def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> UserResponse:
    user = auth_service.authenticate_user(db, email=payload.email, password=payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email 或密碼錯誤")

    session_id = await auth_service.create_session(user)
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_id,
        httponly=True,
        samesite="lax",
        max_age=settings.session_ttl_seconds,
        path="/",
    )
    return UserResponse(id=user.id, email=user.email, display_name=user.display_name)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    _current_user: CurrentUser = Depends(get_current_user),
) -> None:
    session_id = request.cookies.get(settings.session_cookie_name)
    if session_id:
        await auth_service.delete_session(session_id)
    response.delete_cookie(key=settings.session_cookie_name, path="/")


@router.get("/me", response_model=UserResponse, response_model_by_alias=True)
async def me(current_user: CurrentUser = Depends(get_current_user)) -> UserResponse:
    return UserResponse(id=current_user.id, email=current_user.email, display_name=current_user.display_name)
