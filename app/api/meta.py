from fastapi import APIRouter, Depends
from sqlalchemy import distinct, select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models.brand import Brand
from app.models.build import Build
from app.models.component import Component
from app.models.road_model import RoadModel

router = APIRouter(prefix="/meta", tags=["meta"])


def _values(db: Session, stmt):
    return [value for value in db.scalars(stmt).all() if value not in (None, "")]


@router.get("/filters")
def get_filters(db: Session = Depends(get_db_session)):
    return {
        "data": {
            "country_regions": _values(db, select(distinct(Brand.country_region)).order_by(Brand.country_region)),
            "sales_models": _values(db, select(distinct(Brand.sales_model)).order_by(Brand.sales_model)),
            "market_positionings": _values(
                db, select(distinct(Brand.market_positioning)).order_by(Brand.market_positioning)
            ),
            "brand_types": _values(db, select(distinct(Brand.brand_type)).order_by(Brand.brand_type)),
            "brand_names": [
                {"label": brand.brand_name_en, "value": brand.brand_id}
                for brand in db.scalars(select(Brand).order_by(Brand.brand_name_en)).all()
            ],
            "bike_categories": _values(db, select(distinct(RoadModel.bike_category)).order_by(RoadModel.bike_category)),
            "frame_materials": _values(
                db, select(distinct(RoadModel.frame_material)).order_by(RoadModel.frame_material)
            ),
            "brake_types": _values(db, select(distinct(RoadModel.brake_type)).order_by(RoadModel.brake_type)),
            "active_statuses": ["true", "false"],
            "groupset_brands": _values(db, select(distinct(Build.groupset_brand)).order_by(Build.groupset_brand)),
            "wheel_brands": _values(db, select(distinct(Build.wheel_brand)).order_by(Build.wheel_brand)),
            "cockpit_types": _values(db, select(distinct(Build.cockpit_type)).order_by(Build.cockpit_type)),
            "market_regions": _values(db, select(distinct(Build.market_region)).order_by(Build.market_region)),
            "electronic_shifting_options": ["true", "false"],
            "disc_options": ["true", "false"],
            "component_categories": _values(
                db, select(distinct(Component.component_category)).order_by(Component.component_category)
            ),
            "component_brands": _values(db, select(distinct(Component.brand_name)).order_by(Component.brand_name)),
        }
    }
