from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Component(Base):
    __tablename__ = "components"

    component_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    component_category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    brand_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    component_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    series: Mapped[str | None] = mapped_column(String(128), nullable=True)
    weight_g: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    msrp_currency: Mapped[str | None] = mapped_column(String(16), nullable=True)
    msrp_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    official_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
