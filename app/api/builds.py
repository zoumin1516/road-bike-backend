from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.repositories.build_repository import BuildRepository
from app.schemas.build import BuildBase, BuildDetailResponse
from app.schemas.common import PaginationMeta

router = APIRouter(prefix="/builds", tags=["builds"])


@router.get("")
def list_builds(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = None,
    brand_id: str | None = None,
    model_id: str | None = None,
    groupset_brand: str | None = None,
    wheel_brand: str | None = None,
    cockpit_type: str | None = None,
    market_region: str | None = None,
    is_electronic_shifting: bool | None = None,
    is_disc: bool | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db_session),
):
    repo = BuildRepository(db)
    items, total, total_pages = repo.list(
        page=page,
        page_size=page_size,
        keyword=keyword,
        brand_id=brand_id,
        model_id=model_id,
        groupset_brand=groupset_brand,
        wheel_brand=wheel_brand,
        cockpit_type=cockpit_type,
        market_region=market_region,
        is_electronic_shifting=is_electronic_shifting,
        is_disc=is_disc,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
    )
    return {
        "items": [BuildBase.model_validate(item).model_dump() for item in items],
        "pagination": PaginationMeta(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        ).model_dump(),
        "filters": {
            "keyword": keyword,
            "brand_id": brand_id,
            "model_id": model_id,
            "groupset_brand": groupset_brand,
            "wheel_brand": wheel_brand,
            "cockpit_type": cockpit_type,
            "market_region": market_region,
            "is_electronic_shifting": is_electronic_shifting,
            "is_disc": is_disc,
            "min_price": min_price,
            "max_price": max_price,
            "sort": sort,
        },
    }


@router.get("/{build_id}", response_model=BuildDetailResponse)
def get_build(build_id: str, db: Session = Depends(get_db_session)):
    repo = BuildRepository(db)
    item = repo.get_by_id(build_id)
    if not item:
        raise HTTPException(status_code=404, detail="Build not found")
    return {"data": BuildBase.model_validate(item)}
