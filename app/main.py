from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from app.routes import property_router, set_properties
from app.config import settings, scheduler, lifespan


app = FastAPI(
    title="Properties API",
    version=settings.version,
    description="An API for properties",
    lifespan=lifespan,
)
trigger = CronTrigger(hour="12", minute="0")
scheduler.add_job(set_properties, trigger)
scheduler.start()

prefix = f"/api/{settings.api_version}"
app.include_router(router=property_router, prefix=prefix)
