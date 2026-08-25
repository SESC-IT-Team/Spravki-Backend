from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sesc_auth_sdk.routers.auth_router import create_auth_router
from sesc_auth_sdk.settings import AuthRouterSettings

from src.config import settings
from src.routers.user_routes import router as user_router
from src.routers.auth_router import router as auth_router
import uvicorn
from src.db.database import engine, Base
from src.models.order_model import CertificateOrder

app = FastAPI(root_path=settings.ROOT_PATH)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # замените на реальный адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(create_auth_router(AuthRouterSettings(_env_file='.env')), prefix="/auth")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)