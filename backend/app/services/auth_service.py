import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.redis_client import redis_client
from app.core.security import generate_session_id, hash_password, verify_password
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, *, email: str, password: str, display_name: str | None) -> User:
    user = User(email=email, password_hash=hash_password(password), display_name=display_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


async def create_session(user: User) -> str:
    session_id = generate_session_id()
    payload = {
        "user_id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await redis_client.set(f"session:{session_id}", json.dumps(payload), ex=settings.session_ttl_seconds)
    return session_id


async def get_session(session_id: str) -> dict | None:
    raw = await redis_client.get(f"session:{session_id}")
    if raw is None:
        return None
    return json.loads(raw)


async def delete_session(session_id: str) -> None:
    await redis_client.delete(f"session:{session_id}")
