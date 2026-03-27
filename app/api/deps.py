from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import oauth2_scheme
from app.core.security import decode_token
from app.db.session import get_db


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return username
