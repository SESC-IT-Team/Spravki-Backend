from sesc_auth_sdk.dependencies import LyceumAuth, create_jwks_manager_dependency
from sesc_auth_sdk.services.jwks_manager import JWKSManager

from src.config import settings


class Auth(LyceumAuth):
    @staticmethod
    async def get_jwks_manager() -> JWKSManager:
        pass

    get_jwks_manager = create_jwks_manager_dependency(JWKSManager(settings.token_validation_settings))
    user_service_url = settings.user_service_url