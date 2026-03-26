from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.repositories.component_repository import ComponentRepository
from app.schemas.common import PaginationMeta
from app.schemas.component import ComponentBase, ComponentDetailResponse

router = APIRouter(prefix="/components", tags=["components"])


@router.get("")
def list_components(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = None,
    component_category: str | None = None,
    brand_name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db_session),
):
    repo = ComponentRepository(db)
    items, total, total_pages = repo.list(
        page=page,
        page_size=page_size,
        keyword=keyword,
        component_category=component_category,
        brand_name=brand_name,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
    )
    return {
        "items": [ComponentBase.model_validate(item).model_dump() for item in items],
        "pagination": PaginationMeta(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        ).model_dump(),
        "filters": {
            "keyword": keyword,
            "component_category": component_category,
            "brand_name": brand_name,
            "min_price": min_price,
            "max_price": max_price,
            "sort": sort,
        },
    }


@router.get("/{component_id}", response_model=ComponentDetailResponse)
def get_component(component_id: str, db: Session = Depends(get_db_session)):
    repo = ComponentRepository(db)
    item = repo.get_by_id(component_id)
    if not item:
        raise HTTPException(status_code=404, detail="Component not found")
    return {"data": ComponentBase.model_validate(item)}
