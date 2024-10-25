from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


# setting cron
scheduler = BackgroundScheduler()


# defining settings
class Settings(BaseSettings):
    version: str = os.getenv("VERSION", "0.0.0")
    api_version: str = os.getenv("API_VERSION", "v1")
    website_url: str = os.environ.get("WEBSITE_URL")
    user_agent: str = os.environ.get("USER_AGENT")


settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()
