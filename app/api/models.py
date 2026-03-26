from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.repositories.build_repository import BuildRepository
from app.repositories.model_repository import RoadModelRepository
from app.schemas.build import BuildBase
from app.schemas.common import PaginationMeta
from app.schemas.road_model import RoadModelBase, RoadModelDetailResponse

router = APIRouter(prefix="/models", tags=["models"])


@router.get("")
def list_models(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = None,
    brand_id: str | None = None,
    bike_category: str | None = None,
    frame_material: str | None = None,
    brake_type: str | None = None,
    is_active: bool | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db_session),
):
    repo = RoadModelRepository(db)
    items, total, total_pages = repo.list(
        page=page,
        page_size=page_size,
        keyword=keyword,
        brand_id=brand_id,
        bike_category=bike_category,
        frame_material=frame_material,
        brake_type=brake_type,
        is_active=is_active,
        sort=sort,
    )
    return {
        "items": [RoadModelBase.model_validate(item).model_dump() for item in items],
        "pagination": PaginationMeta(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        ).model_dump(),
        "filters": {
            "keyword": keyword,
            "brand_id": brand_id,
            "bike_category": bike_category,
            "frame_material": frame_material,
            "brake_type": brake_type,
            "is_active": is_active,
            "sort": sort,
        },
    }


@router.get("/{model_id}", response_model=RoadModelDetailResponse)
def get_model(model_id: str, db: Session = Depends(get_db_session)):
    repo = RoadModelRepository(db)
    item = repo.get_by_id(model_id)
    if not item:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"data": RoadModelBase.model_validate(item)}


@router.get("/{model_id}/builds")
def list_model_builds(
    model_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_session),
):
    repo = BuildRepository(db)
    items, total, total_pages = repo.list_by_model(model_id, page=page, page_size=page_size)
    return {
        "items": [BuildBase.model_validate(item).model_dump() for item in items],
        "pagination": PaginationMeta(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        ).model_dump(),
        "filters": {"model_id": model_id},
    }
