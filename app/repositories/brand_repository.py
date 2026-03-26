from __future__ import annotations

from math import ceil

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.brand import Brand


class BrandRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        country_region: str | None,
        market_positioning: str | None,
        sales_model: str | None,
        brand_type: str | None,
        sort: str | None,
    ) -> tuple[list[Brand], int, int]:
        stmt: Select[tuple[Brand]] = select(Brand)

        if keyword:
            like = f"%{keyword}%"
            stmt = stmt.where((Brand.brand_name_en.ilike(like)) | (Brand.brand_name_cn.ilike(like)))
        if country_region:
            stmt = stmt.where(Brand.country_region == country_region)
        if market_positioning:
            stmt = stmt.where(Brand.market_positioning == market_positioning)
        if sales_model:
            stmt = stmt.where(Brand.sales_model == sales_model)
        if brand_type:
            stmt = stmt.where(Brand.brand_type == brand_type)

        sort_options = {
            "name_asc": Brand.brand_name_en.asc(),
            "name_desc": Brand.brand_name_en.desc(),
            "country_asc": Brand.country_region.asc(),
            "country_desc": Brand.country_region.desc(),
        }
        order_by = sort_options.get(sort or "name_asc", Brand.brand_name_en.asc())

        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        total_pages = ceil(total / page_size) if total else 0
        items = self.db.scalars(stmt.order_by(order_by).offset((page - 1) * page_size).limit(page_size)).all()
        return items, total, total_pages

    def get_by_id(self, brand_id: str) -> Brand | None:
        return self.db.get(Brand, brand_id)
