from fastapi import APIRouter

from app.api.routes import auth, favorites, health, stations

router = APIRouter()
router.include_router(health.router)
router.include_router(auth.router)
router.include_router(stations.router)
router.include_router(favorites.router)
