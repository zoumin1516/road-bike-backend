from __future__ import annotations

from math import ceil

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.build import Build
from app.models.road_model import RoadModel


class BuildRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        brand_id: str | None,
        model_id: str | None,
        groupset_brand: str | None,
        wheel_brand: str | None,
        cockpit_type: str | None,
        market_region: str | None,
        is_electronic_shifting: bool | None,
        is_disc: bool | None,
        min_price: float | None,
        max_price: float | None,
        sort: str | None,
    ) -> tuple[list[Build], int, int]:
        stmt: Select[tuple[Build]] = select(Build)

        if brand_id:
            stmt = stmt.join(RoadModel, Build.model_id == RoadModel.model_id).where(RoadModel.brand_id == brand_id)
        if keyword:
            like = f"%{keyword}%"
            stmt = stmt.where((Build.build_name.ilike(like)) | (Build.groupset_series.ilike(like)))
        if model_id:
            stmt = stmt.where(Build.model_id == model_id)
        if groupset_brand:
            stmt = stmt.where(Build.groupset_brand == groupset_brand)
        if wheel_brand:
            stmt = stmt.where(Build.wheel_brand == wheel_brand)
        if cockpit_type:
            stmt = stmt.where(Build.cockpit_type == cockpit_type)
        if market_region:
            stmt = stmt.where(Build.market_region == market_region)
        if isinstance(is_electronic_shifting, str):
            normalized = is_electronic_shifting.strip().lower()
            if normalized in {"true", "1", "yes"}:
                is_electronic_shifting = True
            elif normalized in {"false", "0", "no"}:
                is_electronic_shifting = False
            else:
                is_electronic_shifting = None
        if isinstance(is_disc, str):
            normalized = is_disc.strip().lower()
            if normalized in {"true", "1", "yes"}:
                is_disc = True
            elif normalized in {"false", "0", "no"}:
                is_disc = False
            else:
                is_disc = None

        if is_electronic_shifting is not None:
            stmt = stmt.where(Build.is_electronic_shifting == is_electronic_shifting)
        if is_disc is not None:
            stmt = stmt.where(Build.is_disc == is_disc)
        if min_price is not None:
            stmt = stmt.where(Build.msrp_price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Build.msrp_price <= max_price)

        sort_options = {
            "year_desc": Build.model_year.desc(),
            "year_asc": Build.model_year.asc(),
            "price_desc": Build.msrp_price.desc(),
            "price_asc": Build.msrp_price.asc(),
            "name_asc": Build.build_name.asc(),
            "name_desc": Build.build_name.desc(),
        }
        order_by = sort_options.get(sort or "year_desc", Build.model_year.desc())

        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        total_pages = ceil(total / page_size) if total else 0
        items = self.db.scalars(stmt.order_by(order_by).offset((page - 1) * page_size).limit(page_size)).all()
        return items, total, total_pages

    def get_by_id(self, build_id: str) -> Build | None:
        return self.db.get(Build, build_id)

    def list_by_model(self, model_id: str, *, page: int, page_size: int) -> tuple[list[Build], int, int]:
        stmt: Select[tuple[Build]] = select(Build).where(Build.model_id == model_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        total_pages = ceil(total / page_size) if total else 0
        items = self.db.scalars(
            stmt.order_by(Build.model_year.desc(), Build.build_name.asc()).offset((page - 1) * page_size).limit(page_size)
        ).all()
        return items, total, total_pages
