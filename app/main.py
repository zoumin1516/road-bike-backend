from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, admin_entities, admin_media, auth, brands, builds, components, meta, models, search
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(admin_entities.router, prefix="/api")
app.include_router(admin_media.router, prefix="/api")
app.include_router(brands.router, prefix="/api")
app.include_router(models.router, prefix="/api")
app.include_router(builds.router, prefix="/api")
app.include_router(components.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(meta.router, prefix="/api")
