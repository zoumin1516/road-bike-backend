from pydantic import BaseModel, ConfigDict


class ComponentBase(BaseModel):
    component_id: str
    component_category: str
    brand_name: str
    component_name: str
    series: str | None = None
    weight_g: float | None = None
    msrp_currency: str | None = None
    msrp_price: float | None = None
    official_url: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ComponentDetailResponse(BaseModel):
    data: ComponentBase
