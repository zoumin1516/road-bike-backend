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
    headquarters: str | None = None
    founded_year: str | None = None
    founder: str | None = None
    parent_company: str | None = None
    company_type: str | None = None
    ownership_type: str | None = None
    road_cycling_positioning: str | None = None
    target_audience: str | None = None
    price_tier: str | None = None
    brand_slogan: str | None = None
    brand_story: str | None = None
    mission: str | None = None
    core_values: str | None = None
    core_technologies: str | None = None
    r_and_d_capabilities: str | None = None
    flagship_platforms: str | None = None
    employee_count_range: str | None = None
    annual_revenue_range: str | None = None
    product_lines: str | None = None
    road_product_lines: str | None = None
    data_sources: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class BrandSummary(BrandBase):
    pass


class BrandDetailResponse(BaseModel):
    data: BrandBase
