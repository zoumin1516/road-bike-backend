from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RoadModel(Base):
    __tablename__ = "models"

    model_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    brand_id: Mapped[str] = mapped_column(ForeignKey("brands.brand_id"), nullable=False, index=True)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    series_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    bike_category: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    frame_material: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    brake_type: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    tire_clearance_mm: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    release_year_first: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_generation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    official_model_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    brand: Mapped["Brand"] = relationship(back_populates="models")
    builds: Mapped[list["Build"]] = relationship(back_populates="model")
