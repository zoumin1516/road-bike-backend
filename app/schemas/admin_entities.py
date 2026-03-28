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


class BuildUpdateRequest(BaseModel):
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
    is_disc: bool = True
    is_electronic_shifting: bool = False
    is_stock_complete_bike: bool = True
    official_build_url: HttpUrl | None = None
    notes: str | None = None


class BuildUpdateResponse(BaseModel):
    status: str
    message: str
    data: dict[str, str | None]


class ComponentUpdateRequest(BaseModel):
    component_category: str
    brand_name: str
    component_name: str
    series: str | None = None
    weight_g: float | None = None
    msrp_currency: str | None = None
    msrp_price: float | None = None
    official_url: HttpUrl | None = None
    notes: str | None = None


class ComponentUpdateResponse(BaseModel):
    status: str
    message: str
    data: dict[str, str | None]
