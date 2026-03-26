from __future__ import annotations

from math import ceil

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.road_model import RoadModel


class RoadModelRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        brand_id: str | None,
        bike_category: str | None,
        frame_material: str | None,
        brake_type: str | None,
        is_active: bool | None,
        sort: str | None,
    ) -> tuple[list[RoadModel], int, int]:
        stmt: Select[tuple[RoadModel]] = select(RoadModel)

        if keyword:
            like = f"%{keyword}%"
            stmt = stmt.where(RoadModel.model_name.ilike(like))
        if brand_id:
            stmt = stmt.where(RoadModel.brand_id == brand_id)
        if bike_category:
            stmt = stmt.where(RoadModel.bike_category == bike_category)
        if frame_material:
            stmt = stmt.where(RoadModel.frame_material == frame_material)
        if brake_type:
            stmt = stmt.where(RoadModel.brake_type == brake_type)
        if is_active is not None:
            stmt = stmt.where(RoadModel.is_active == is_active)

        sort_options = {
            "name_asc": RoadModel.model_name.asc(),
            "name_desc": RoadModel.model_name.desc(),
            "year_desc": RoadModel.release_year_first.desc(),
            "year_asc": RoadModel.release_year_first.asc(),
            "active_desc": RoadModel.is_active.desc(),
            "active_asc": RoadModel.is_active.asc(),
        }
        order_by = sort_options.get(sort or "name_asc", RoadModel.model_name.asc())

        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        total_pages = ceil(total / page_size) if total else 0
        items = self.db.scalars(stmt.order_by(order_by).offset((page - 1) * page_size).limit(page_size)).all()
        return items, total, total_pages

    def get_by_id(self, model_id: str) -> RoadModel | None:
        return self.db.get(RoadModel, model_id)

    def list_by_brand(self, brand_id: str, *, page: int, page_size: int) -> tuple[list[RoadModel], int, int]:
        stmt: Select[tuple[RoadModel]] = select(RoadModel).where(RoadModel.brand_id == brand_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        total_pages = ceil(total / page_size) if total else 0
        items = self.db.scalars(
            stmt.order_by(RoadModel.model_name.asc()).offset((page - 1) * page_size).limit(page_size)
        ).all()
        return items, total, total_pages
