from fastapi import APIRouter, Depends

from app.api.deps import get_current_username

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ping")
def admin_ping(username: str = Depends(get_current_username)):
    return {"status": "ok", "username": username}
