from pydantic import BaseModel, ConfigDict


class BuildBase(BaseModel):
    build_id: str
    model_id: str
    build_name: str
    model_year: int | None = None
    market_region: str | None = None
    msrp_currency: str | None = None
    msrp_price: float | None = None
    groupset_brand: str | None = None
    groupset_series: str | None = None
    wheel_brand: str | None = None
    wheel_model: str | None = None
    power_meter: str | None = None
    cockpit_type: str | None = None
    claimed_weight_kg: float | None = None
    is_disc: bool
    is_electronic_shifting: bool
    is_stock_complete_bike: bool
    official_build_url: str | None = None
    image_url: str | None = None
    hero_image_url: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class BuildDetailResponse(BaseModel):
    data: BuildBase
