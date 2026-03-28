from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Brand(Base):
    __tablename__ = "brands"

    brand_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    brand_name_en: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    brand_name_cn: Mapped[str | None] = mapped_column(String(128), nullable=True)
    country_region: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    brand_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    market_positioning: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    sales_model: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    main_road_categories: Mapped[str | None] = mapped_column(String(255), nullable=True)
    official_website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    hero_image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    headquarters: Mapped[str | None] = mapped_column(String(255), nullable=True)
    founded_year: Mapped[str | None] = mapped_column(String(32), nullable=True)
    founder: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parent_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    ownership_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    road_cycling_positioning: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_audience: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price_tier: Mapped[str | None] = mapped_column(String(128), nullable=True)
    brand_slogan: Mapped[str | None] = mapped_column(String(255), nullable=True)
    brand_story: Mapped[str | None] = mapped_column(Text, nullable=True)
    mission: Mapped[str | None] = mapped_column(Text, nullable=True)
    core_values: Mapped[str | None] = mapped_column(Text, nullable=True)
    core_technologies: Mapped[str | None] = mapped_column(Text, nullable=True)
    r_and_d_capabilities: Mapped[str | None] = mapped_column(Text, nullable=True)
    flagship_platforms: Mapped[str | None] = mapped_column(Text, nullable=True)
    employee_count_range: Mapped[str | None] = mapped_column(String(128), nullable=True)
    annual_revenue_range: Mapped[str | None] = mapped_column(String(128), nullable=True)
    product_lines: Mapped[str | None] = mapped_column(Text, nullable=True)
    road_product_lines: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_sources: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    models: Mapped[list["RoadModel"]] = relationship(back_populates="brand")
