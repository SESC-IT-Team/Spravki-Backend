from fastapi import FastAPI
from sesc_auth_sdk.routers.auth_router import create_auth_router
from sesc_auth_sdk.settings import AuthRouterSettings

from src.config import settings
from src.routers.user_routes import router as user_router
from src.routers.auth_router import router as auth_router
import uvicorn
from src.db.database import engine, Base
from src.models.order_model import CertificateOrder

app = FastAPI(root_path=settings.ROOT_PATH)
app.include_router(user_router)
app.include_router(create_auth_router(AuthRouterSettings(_env_file='.env')))



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)