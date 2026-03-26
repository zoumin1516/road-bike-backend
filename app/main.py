from fastapi import FastAPI

from app.api import brands, builds, components, meta, models, search
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(brands.router, prefix="/api")
app.include_router(models.router, prefix="/api")
app.include_router(builds.router, prefix="/api")
app.include_router(components.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(meta.router, prefix="/api")
