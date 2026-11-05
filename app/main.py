from fastapi import FastAPI

from app.infrastructure.config import get_settings
from app.presentation.api.handlers import register_exception_handlers
from app.presentation.api.routes import router as api_router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.api.title,
        debug=settings.api.debug,
    )
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
