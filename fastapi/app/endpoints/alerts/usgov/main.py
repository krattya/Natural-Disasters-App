from fastapi import APIRouter, Request
import app.endpoints.alerts.usgov.crud as usgov_crud

router = APIRouter()


@router.get("")
def get_usgov_alerts(request: Request):
    return usgov_crud.get_all_usgov_alerts(request)


@router.get("/{alert_id_usgov}/")
def get_usgov_alert(request: Request, alert_id_usgov: str):
    return usgov_crud.get_usgov_alert(alert_id_usgov, request)
