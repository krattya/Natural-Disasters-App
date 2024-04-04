from fastapi import APIRouter, Request
import app.endpoints.alerts.gdacs.crud as crud_gdacs

router = APIRouter()


@router.get("")
def get_all_gdacs_alerts(request: Request):
    return crud_gdacs.get_all_gdacs_alerts(request)


@router.get("/{alert_id_gdac}/")
def get_gdacs_alert(alert_id_gdac: str, request: Request):
    return crud_gdacs.get_gdacs_alert(alert_id_gdac, request)
