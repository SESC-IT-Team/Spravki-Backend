from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from sesc_auth_sdk.settings import AuthRouterSettings, TokenValidationSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env", env_file_encoding="utf-8", extra="ignore")

    allowed_origins: list[str]

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ROOT_PATH: str = '/'

    auth_router_config: AuthRouterSettings = AuthRouterSettings(_env_file='.env')
    token_validation_settings: TokenValidationSettings = TokenValidationSettings(_env_file='.env')
    user_service_url: str


settings = Settings()