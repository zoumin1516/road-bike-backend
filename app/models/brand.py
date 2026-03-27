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
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    models: Mapped[list["RoadModel"]] = relationship(back_populates="brand")
