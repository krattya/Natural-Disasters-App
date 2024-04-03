from fastapi import APIRouter
from app.endpoints.alerts.main import router as alerts_router
from app.endpoints.predictions.main import router as predictions_router
from app.endpoints.alerts.gdacs.main import router as gdacs_router

router = APIRouter()

router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
router.include_router(predictions_router, prefix="/predictions", tags=["predictions"])
router.include_router(gdacs_router, prefix="/alerts/gdacs", tags=["alerts_gdacs"])
