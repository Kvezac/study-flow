from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.infrastructure.config import get_settings

settings = get_settings()
engine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo,
    future=True,
)
SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)
