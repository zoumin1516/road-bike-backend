from pydantic import BaseModel, HttpUrl


class BrandMediaUpdateRequest(BaseModel):
    logo_url: HttpUrl | None = None
    hero_image_url: HttpUrl | None = None


class ItemMediaUpdateRequest(BaseModel):
    image_url: HttpUrl | None = None
    hero_image_url: HttpUrl | None = None


class AdminMutationResponse(BaseModel):
    status: str = "ok"
    message: str
