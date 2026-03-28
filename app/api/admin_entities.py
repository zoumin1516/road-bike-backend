from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_username, get_db_session
from app.models.brand import Brand
from app.models.build import Build
from app.models.component import Component
from app.models.road_model import RoadModel
from app.schemas.admin_entities import (
    BrandUpdateRequest,
    BrandUpdateResponse,
    BuildUpdateRequest,
    BuildUpdateResponse,
    ComponentUpdateRequest,
    ComponentUpdateResponse,
    ModelUpdateRequest,
    ModelUpdateResponse,
)

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
    brand.headquarters = payload.headquarters
    brand.founded_year = payload.founded_year
    brand.founder = payload.founder
    brand.parent_company = payload.parent_company
    brand.company_type = payload.company_type
    brand.ownership_type = payload.ownership_type
    brand.road_cycling_positioning = payload.road_cycling_positioning
    brand.target_audience = payload.target_audience
    brand.price_tier = payload.price_tier
    brand.brand_slogan = payload.brand_slogan
    brand.brand_story = payload.brand_story
    brand.mission = payload.mission
    brand.core_values = payload.core_values
    brand.core_technologies = payload.core_technologies
    brand.r_and_d_capabilities = payload.r_and_d_capabilities
    brand.flagship_platforms = payload.flagship_platforms
    brand.employee_count_range = payload.employee_count_range
    brand.annual_revenue_range = payload.annual_revenue_range
    brand.product_lines = payload.product_lines
    brand.road_product_lines = payload.road_product_lines
    brand.data_sources = payload.data_sources
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
            "headquarters": brand.headquarters,
            "founded_year": brand.founded_year,
            "founder": brand.founder,
            "parent_company": brand.parent_company,
            "company_type": brand.company_type,
            "ownership_type": brand.ownership_type,
            "road_cycling_positioning": brand.road_cycling_positioning,
            "target_audience": brand.target_audience,
            "price_tier": brand.price_tier,
            "brand_slogan": brand.brand_slogan,
            "brand_story": brand.brand_story,
            "mission": brand.mission,
            "core_values": brand.core_values,
            "core_technologies": brand.core_technologies,
            "r_and_d_capabilities": brand.r_and_d_capabilities,
            "flagship_platforms": brand.flagship_platforms,
            "employee_count_range": brand.employee_count_range,
            "annual_revenue_range": brand.annual_revenue_range,
            "product_lines": brand.product_lines,
            "road_product_lines": brand.road_product_lines,
            "data_sources": brand.data_sources,
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


@router.put("/builds/{build_id}", response_model=BuildUpdateResponse)
def update_build(
    build_id: str,
    payload: BuildUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    item = db.get(Build, build_id)
    if not item:
        raise HTTPException(status_code=404, detail="Build not found")

    item.build_name = payload.build_name
    item.model_year = payload.model_year
    item.market_region = payload.market_region
    item.msrp_currency = payload.msrp_currency
    item.msrp_price = payload.msrp_price
    item.groupset_brand = payload.groupset_brand
    item.groupset_series = payload.groupset_series
    item.wheel_brand = payload.wheel_brand
    item.wheel_model = payload.wheel_model
    item.power_meter = payload.power_meter
    item.cockpit_type = payload.cockpit_type
    item.claimed_weight_kg = payload.claimed_weight_kg
    item.is_disc = payload.is_disc
    item.is_electronic_shifting = payload.is_electronic_shifting
    item.is_stock_complete_bike = payload.is_stock_complete_bike
    item.official_build_url = str(payload.official_build_url) if payload.official_build_url else None
    item.notes = payload.notes

    db.add(item)
    db.commit()
    db.refresh(item)

    return BuildUpdateResponse(
        status="ok",
        message=f"Updated build {build_id}",
        data={
            "build_id": item.build_id,
            "build_name": item.build_name,
            "model_year": str(item.model_year) if item.model_year is not None else None,
            "market_region": item.market_region,
            "msrp_currency": item.msrp_currency,
            "msrp_price": str(item.msrp_price) if item.msrp_price is not None else None,
            "groupset_brand": item.groupset_brand,
            "groupset_series": item.groupset_series,
            "wheel_brand": item.wheel_brand,
            "wheel_model": item.wheel_model,
            "power_meter": item.power_meter,
            "cockpit_type": item.cockpit_type,
            "claimed_weight_kg": str(item.claimed_weight_kg) if item.claimed_weight_kg is not None else None,
            "is_disc": str(item.is_disc),
            "is_electronic_shifting": str(item.is_electronic_shifting),
            "is_stock_complete_bike": str(item.is_stock_complete_bike),
            "official_build_url": item.official_build_url,
            "notes": item.notes,
        },
    )


@router.put("/components/{component_id}", response_model=ComponentUpdateResponse)
def update_component(
    component_id: str,
    payload: ComponentUpdateRequest,
    db: Session = Depends(get_db_session),
    _: str = Depends(get_current_username),
):
    item = db.get(Component, component_id)
    if not item:
        raise HTTPException(status_code=404, detail="Component not found")

    item.component_category = payload.component_category
    item.brand_name = payload.brand_name
    item.component_name = payload.component_name
    item.series = payload.series
    item.weight_g = payload.weight_g
    item.msrp_currency = payload.msrp_currency
    item.msrp_price = payload.msrp_price
    item.official_url = str(payload.official_url) if payload.official_url else None
    item.notes = payload.notes

    db.add(item)
    db.commit()
    db.refresh(item)

    return ComponentUpdateResponse(
        status="ok",
        message=f"Updated component {component_id}",
        data={
            "component_id": item.component_id,
            "component_category": item.component_category,
            "brand_name": item.brand_name,
            "component_name": item.component_name,
            "series": item.series,
            "weight_g": str(item.weight_g) if item.weight_g is not None else None,
            "msrp_currency": item.msrp_currency,
            "msrp_price": str(item.msrp_price) if item.msrp_price is not None else None,
            "official_url": item.official_url,
            "notes": item.notes,
        },
    )
