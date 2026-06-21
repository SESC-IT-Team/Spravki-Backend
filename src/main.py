from fastapi import FastAPI

from src.config import settings
from src.routers.user_routes import router as user_router
import uvicorn
from src.db.database import engine, Base
from src.models.order_model import CertificateOrder

app = FastAPI(root_path=settings.ROOT_PATH)
app.include_router(user_router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)