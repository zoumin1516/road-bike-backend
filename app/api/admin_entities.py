from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_username, get_db_session
from app.models.brand import Brand
from app.models.road_model import RoadModel
from app.schemas.admin_entities import BrandUpdateRequest, BrandUpdateResponse, ModelUpdateRequest, ModelUpdateResponse

router = APIRouter(prefix="/admin/entities", tags=["admin-entities"])


@router.put("/brands/{brand_id}", response_model=BrandUpdateResponse)
def update_brand(
    brand_id: str,
    payload: BrandUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    brand.brand_name_en = payload.brand_name_en
    brand.brand_name_cn = payload.brand_name_cn
    brand.country_region = payload.country_region
    brand.brand_type = payload.brand_type
    brand.market_positioning = payload.market_positioning
    brand.sales_model = payload.sales_model
    brand.main_road_categories = payload.main_road_categories
    brand.official_website = str(payload.official_website) if payload.official_website else None
    brand.notes = payload.notes

    db.add(brand)
    db.commit()
    db.refresh(brand)

    return BrandUpdateResponse(
        status="ok",
        message=f"Updated brand {brand_id}",
        data={
            "brand_id": brand.brand_id,
            "brand_name_en": brand.brand_name_en,
            "brand_name_cn": brand.brand_name_cn,
            "country_region": brand.country_region,
            "brand_type": brand.brand_type,
            "market_positioning": brand.market_positioning,
            "sales_model": brand.sales_model,
            "main_road_categories": brand.main_road_categories,
            "official_website": brand.official_website,
            "notes": brand.notes,
        },
    )


@router.put("/models/{model_id}", response_model=ModelUpdateResponse)
def update_model(
    model_id: str,
    payload: ModelUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    item = db.get(RoadModel, model_id)
    if not item:
        raise HTTPException(status_code=404, detail="Model not found")

    item.model_name = payload.model_name
    item.series_name = payload.series_name
    item.bike_category = payload.bike_category
    item.frame_material = payload.frame_material
    item.brake_type = payload.brake_type
    item.release_year_first = payload.release_year_first
    item.current_generation_year = payload.current_generation_year
    item.official_model_url = str(payload.official_model_url) if payload.official_model_url else None
    item.notes = payload.notes

    db.add(item)
    db.commit()
    db.refresh(item)

    return ModelUpdateResponse(
        status="ok",
        message=f"Updated model {model_id}",
        data={
            "model_id": item.model_id,
            "model_name": item.model_name,
            "series_name": item.series_name,
            "bike_category": item.bike_category,
            "frame_material": item.frame_material,
            "brake_type": item.brake_type,
            "release_year_first": str(item.release_year_first) if item.release_year_first is not None else None,
            "current_generation_year": str(item.current_generation_year) if item.current_generation_year is not None else None,
            "official_model_url": item.official_model_url,
            "notes": item.notes,
        },
    )
