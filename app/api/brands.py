from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.repositories.brand_repository import BrandRepository
from app.repositories.model_repository import RoadModelRepository
from app.schemas.brand import BrandDetailResponse, BrandSummary
from app.schemas.common import PaginationMeta
from app.schemas.road_model import RoadModelBase

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("")
def list_brands(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = None,
    country_region: str | None = None,
    market_positioning: str | None = None,
    sales_model: str | None = None,
    brand_type: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db_session),
):
    repo = BrandRepository(db)
    items, total, total_pages = repo.list(
        page=page,
        page_size=page_size,
        keyword=keyword,
        country_region=country_region,
        market_positioning=market_positioning,
        sales_model=sales_model,
        brand_type=brand_type,
        sort=sort,
    )
    return {
        "items": [BrandSummary.model_validate(item).model_dump() for item in items],
        "pagination": PaginationMeta(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        ).model_dump(),
        "filters": {
            "keyword": keyword,
            "country_region": country_region,
            "market_positioning": market_positioning,
            "sales_model": sales_model,
            "brand_type": brand_type,
            "sort": sort,
        },
    }


@router.get("/{brand_id}", response_model=BrandDetailResponse)
def get_brand(brand_id: str, db: Session = Depends(get_db_session)):
    repo = BrandRepository(db)
    brand = repo.get_by_id(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"data": BrandSummary.model_validate(brand)}


@router.get("/{brand_id}/models")
def list_brand_models(
    brand_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_session),
):
    repo = RoadModelRepository(db)
    items, total, total_pages = repo.list_by_brand(brand_id, page=page, page_size=page_size)
    return {
        "items": [RoadModelBase.model_validate(item).model_dump() for item in items],
        "pagination": PaginationMeta(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        ).model_dump(),
        "filters": {"brand_id": brand_id},
    }
