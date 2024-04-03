from fastapi import APIRouter, Request
import app.endpoints.alerts.gdacs.crud as crud_gdacs

router = APIRouter()


@router.get("/{alert_id_gdac}/")
def get_gdac_alert(alert_id_gdac: str, request: Request):
    return crud_gdacs.get_gdac_alert(alert_id_gdac, request)
