from fastapi import FastAPI
from src.routers.user_routers import router as user_router
import uvicorn
app = FastAPI()
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)