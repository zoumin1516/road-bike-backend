from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models.brand import Brand
from app.models.build import Build
from app.models.component import Component
from app.models.road_model import RoadModel
from app.schemas.common import PaginationMeta

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def global_search(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: str | None = None,
    db: Session = Depends(get_db_session),
):
    like = f"%{q}%"
    items: list[dict[str, str]] = []

    if type in (None, "brand"):
        brands = db.scalars(
            select(Brand).where(or_(Brand.brand_name_en.ilike(like), Brand.brand_name_cn.ilike(like))).limit(page_size)
        ).all()
        items.extend(
            {
                "type": "brand",
                "id": item.brand_id,
                "title": item.brand_name_en,
                "subtitle": item.country_region or "Brand",
            }
            for item in brands
        )

    if type in (None, "model") and len(items) < page_size:
        remaining = page_size - len(items)
        models = db.scalars(
            select(RoadModel).where(or_(RoadModel.model_name.ilike(like), RoadModel.series_name.ilike(like))).limit(remaining)
        ).all()
        items.extend(
            {
                "type": "model",
                "id": item.model_id,
                "title": item.model_name,
                "subtitle": item.bike_category or "Model",
            }
            for item in models
        )

    if type in (None, "build") and len(items) < page_size:
        remaining = page_size - len(items)
        builds = db.scalars(
            select(Build).where(
                or_(
                    Build.build_name.ilike(like),
                    Build.groupset_brand.ilike(like),
                    Build.groupset_series.ilike(like),
                    Build.wheel_brand.ilike(like),
                    Build.wheel_model.ilike(like),
                )
            ).limit(remaining)
        ).all()
        items.extend(
            {
                "type": "build",
                "id": item.build_id,
                "title": item.build_name,
                "subtitle": item.groupset_series or item.groupset_brand or "Build",
            }
            for item in builds
        )

    if type in (None, "component") and len(items) < page_size:
        remaining = page_size - len(items)
        components = db.scalars(
            select(Component).where(
                or_(
                    Component.component_name.ilike(like),
                    Component.brand_name.ilike(like),
                    Component.series.ilike(like),
                )
            ).limit(remaining)
        ).all()
        items.extend(
            {
                "type": "component",
                "id": item.component_id,
                "title": item.component_name,
                "subtitle": item.series or item.component_category,
            }
            for item in components
        )

    items = items[:page_size]
    total = len(items)
    return {
        "items": items,
        "pagination": PaginationMeta(page=page, page_size=page_size, total=total, total_pages=1).model_dump(),
        "filters": {"q": q, "type": type},
    }
