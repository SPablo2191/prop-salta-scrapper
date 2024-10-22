from fastapi import FastAPI
from app.routes import property_router
from app.config import settings

app = FastAPI(
    title="Properties API",
    version=settings.version,
    description="An API for properties",
)
prefix = f"/api/{settings.api_version}"
app.include_router(router=property_router, prefix=prefix)
