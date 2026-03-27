from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Build(Base):
    __tablename__ = "builds"

    build_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    model_id: Mapped[str] = mapped_column(ForeignKey("models.model_id"), nullable=False, index=True)
    build_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    model_year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    market_region: Mapped[str | None] = mapped_column(String(64), nullable=True)
    msrp_currency: Mapped[str | None] = mapped_column(String(16), nullable=True)
    msrp_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, index=True)
    groupset_brand: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    groupset_series: Mapped[str | None] = mapped_column(String(128), nullable=True)
    wheel_brand: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    wheel_model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    power_meter: Mapped[str | None] = mapped_column(String(64), nullable=True)
    cockpit_type: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    claimed_weight_kg: Mapped[float | None] = mapped_column(Numeric(6, 3), nullable=True)
    is_disc: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_electronic_shifting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    is_stock_complete_bike: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    official_build_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    hero_image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    model: Mapped["RoadModel"] = relationship(back_populates="builds")
