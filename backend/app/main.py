import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings
from app.exceptions import unhandled_exception_handler

app = FastAPI(title="YouBike 即時資訊系統 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(api_router, prefix="/api")

WEB_SERVER_SETTING = {
    "app": "app.main:app",
    "host": "0.0.0.0",
    "port": 8000,
    "reload": settings.app_env == "development",
}

if __name__ == "__main__":
    uvicorn.run(**WEB_SERVER_SETTING)
