from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    title: str
    debug: bool
    prefix: str


class DatabaseSettings(BaseModel):
    url: str
    echo: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(default="development", validation_alias="APP_ENV")
    app_title: str = Field(default="FastAPI Education", validation_alias="APP_TITLE")
    app_debug: bool = Field(default=True, validation_alias="APP_DEBUG")
    api_prefix: str = Field(default="/api", validation_alias="API_PREFIX")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./fastapi_education.db",
        validation_alias="DATABASE_URL",
    )
    database_echo: bool = Field(default=False, validation_alias="DATABASE_ECHO")

    @property
    def api(self) -> ApiSettings:
        return ApiSettings(
            title=self.app_title,
            debug=self.app_debug,
            prefix=self.api_prefix,
        )

    @property
    def database(self) -> DatabaseSettings:
        return DatabaseSettings(
            url=self.database_url,
            echo=self.database_echo,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
