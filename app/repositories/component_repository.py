from __future__ import annotations

from math import ceil

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.component import Component


class ComponentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        component_category: str | None,
        brand_name: str | None,
        min_price: float | None,
        max_price: float | None,
        sort: str | None,
    ) -> tuple[list[Component], int, int]:
        stmt: Select[tuple[Component]] = select(Component)

        if keyword:
            like = f"%{keyword}%"
            stmt = stmt.where((Component.component_name.ilike(like)) | (Component.series.ilike(like)))
        if component_category:
            stmt = stmt.where(Component.component_category == component_category)
        if brand_name:
            stmt = stmt.where(Component.brand_name == brand_name)
        if min_price is not None:
            stmt = stmt.where(Component.msrp_price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Component.msrp_price <= max_price)

        sort_options = {
            "name_asc": Component.component_name.asc(),
            "name_desc": Component.component_name.desc(),
            "price_desc": Component.msrp_price.desc(),
            "price_asc": Component.msrp_price.asc(),
            "brand_asc": Component.brand_name.asc(),
            "brand_desc": Component.brand_name.desc(),
        }
        order_by = sort_options.get(sort or "name_asc", Component.component_name.asc())

        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        total_pages = ceil(total / page_size) if total else 0
        items = self.db.scalars(stmt.order_by(order_by).offset((page - 1) * page_size).limit(page_size)).all()
        return items, total, total_pages

    def get_by_id(self, component_id: str) -> Component | None:
        return self.db.get(Component, component_id)
