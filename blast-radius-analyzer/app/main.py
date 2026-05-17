from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.analyze import router as analyze_router
from app.api.github_webhook import router as github_webhook_router
from app.api.health import router as health_router
from app.api.replay import router as replay_router
from app.core.bootstrap import bootstrap_app
from app.core.config import get_settings
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Run startup initialization for the app."""
    configure_logging()
    bootstrap_app()
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(health_router)
app.include_router(replay_router)
app.include_router(analyze_router)
app.include_router(github_webhook_router)
