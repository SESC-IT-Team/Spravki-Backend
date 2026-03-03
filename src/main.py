from fastapi import FastAPI
from src.routers.user_routes import router as user_router
import uvicorn
from src.db.database import engine, Base
from src.models.order_model import CertificateOrder

app = FastAPI()
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)