from fastapi import APIRouter, Request
import app.endpoints.alerts.crud as crud_alerts
from typing import List
from app.endpoints.alerts.models import AlertInDB

router = APIRouter()


@router.get("/", response_model=List[AlertInDB])
def get_all_alerts(request: Request):
    return crud_alerts.get_all_alerts(request.app.db)


@router.get("/{alert_id}/")
def get_alert_by_id(alert_id: str, request: Request):
    return crud_alerts.get_alert_by_id(alert_id, request.app.db)
