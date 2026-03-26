from pydantic import BaseModel, ConfigDict


class RoadModelBase(BaseModel):
    model_id: str
    brand_id: str
    model_name: str
    series_name: str | None = None
    bike_category: str | None = None
    frame_material: str | None = None
    brake_type: str | None = None
    tire_clearance_mm: float | None = None
    release_year_first: int | None = None
    current_generation_year: int | None = None
    is_active: bool
    official_model_url: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RoadModelDetailResponse(BaseModel):
    data: RoadModelBase
