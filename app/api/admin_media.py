from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_username, get_db_session
from app.models.brand import Brand
from app.models.build import Build
from app.models.component import Component
from app.models.road_model import RoadModel
from app.schemas.admin import AdminMutationResponse, BrandMediaUpdateRequest, ItemMediaUpdateRequest

router = APIRouter(prefix="/admin/media", tags=["admin-media"])


@router.put("/brands/{brand_id}", response_model=AdminMutationResponse)
def update_brand_media(
    brand_id: str,
    payload: BrandMediaUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    brand.logo_url = str(payload.logo_url) if payload.logo_url else None
    brand.hero_image_url = str(payload.hero_image_url) if payload.hero_image_url else None
    db.add(brand)
    db.commit()
    return AdminMutationResponse(message=f"Updated media for brand {brand_id}")


@router.put("/models/{model_id}", response_model=AdminMutationResponse)
def update_model_media(
    model_id: str,
    payload: ItemMediaUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    item = db.get(RoadModel, model_id)
    if not item:
        raise HTTPException(status_code=404, detail="Model not found")

    item.image_url = str(payload.image_url) if payload.image_url else None
    item.hero_image_url = str(payload.hero_image_url) if payload.hero_image_url else None
    db.add(item)
    db.commit()
    return AdminMutationResponse(message=f"Updated media for model {model_id}")


@router.put("/builds/{build_id}", response_model=AdminMutationResponse)
def update_build_media(
    build_id: str,
    payload: ItemMediaUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    item = db.get(Build, build_id)
    if not item:
        raise HTTPException(status_code=404, detail="Build not found")

    item.image_url = str(payload.image_url) if payload.image_url else None
    item.hero_image_url = str(payload.hero_image_url) if payload.hero_image_url else None
    db.add(item)
    db.commit()
    return AdminMutationResponse(message=f"Updated media for build {build_id}")


@router.put("/components/{component_id}", response_model=AdminMutationResponse)
def update_component_media(
    component_id: str,
    payload: ItemMediaUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    item = db.get(Component, component_id)
    if not item:
        raise HTTPException(status_code=404, detail="Component not found")

    item.image_url = str(payload.image_url) if payload.image_url else None
    item.hero_image_url = str(payload.hero_image_url) if payload.hero_image_url else None
    db.add(item)
    db.commit()
    return AdminMutationResponse(message=f"Updated media for component {component_id}")
