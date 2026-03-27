from pydantic import BaseModel, HttpUrl


class BrandUpdateRequest(BaseModel):
    brand_name_en: str
    brand_name_cn: str | None = None
    country_region: str | None = None
    brand_type: str | None = None
    market_positioning: str | None = None
    sales_model: str | None = None
    main_road_categories: str | None = None
    official_website: HttpUrl | None = None
    notes: str | None = None


class BrandUpdateResponse(BaseModel):
    status: str
    message: str
    data: dict[str, str | None]


class ModelUpdateRequest(BaseModel):
    model_name: str
    series_name: str | None = None
    bike_category: str | None = None
    frame_material: str | None = None
    brake_type: str | None = None
    release_year_first: int | None = None
    current_generation_year: int | None = None
    official_model_url: HttpUrl | None = None
    notes: str | None = None


class ModelUpdateResponse(BaseModel):
    status: str
    message: str
    data: dict[str, str | None]
