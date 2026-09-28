from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status

from app.core.config import settings
from app.services import auth_service


@dataclass
class CurrentUser:
    id: int
    email: str
    display_name: str | None


async def get_current_user(request: Request) -> CurrentUser:
    session_id = request.cookies.get(settings.session_cookie_name)
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登入")

    session = await auth_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登入已過期，請重新登入")

    return CurrentUser(id=session["user_id"], email=session["email"], display_name=session.get("display_name"))
