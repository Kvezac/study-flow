from fastapi import FastAPI

from app.infrastructure.config import get_settings
from app.presentation.api.handlers import register_exception_handlers
from app.presentation.api.routes import router as api_router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.api.title,
        debug=settings.api.debug,
        description=(
            "Online school API built with clean architecture. "
            "At the first stage, the application supports public content reading "
            "and administrative management of courses, modules, sections and lectures."
        ),
        version="1.0.0",
        openapi_tags=[
            {
                "name": "Content",
                "description": "Public endpoints for reading courses, course structure and lectures.",
            },
            {
                "name": "Admin",
                "description": "Administrative endpoints for creating and updating content.",
            },
            {
                "name": "Auth",
                "description": "Endpoints for user registration and login with JWT token issuing.",
            },
        ],
    )
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
