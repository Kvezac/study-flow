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


class JwtSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
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
    jwt_secret_key: str = Field(default="...", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )

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

    @property
    def jwt(self) -> JwtSettings:
        return JwtSettings(
            secret_key=self.jwt_secret_key,
            algorithm=self.jwt_algorithm,
            access_token_expire_minutes=self.jwt_access_token_expire_minutes,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
