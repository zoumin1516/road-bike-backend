from pydantic import BaseModel, ConfigDict


class BrandBase(BaseModel):
    brand_id: str
    brand_name_en: str
    brand_name_cn: str | None = None
    country_region: str | None = None
    brand_type: str | None = None
    market_positioning: str | None = None
    sales_model: str | None = None
    main_road_categories: str | None = None
    official_website: str | None = None
    logo_url: str | None = None
    hero_image_url: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class BrandSummary(BrandBase):
    pass


class BrandDetailResponse(BaseModel):
    data: BrandBase
