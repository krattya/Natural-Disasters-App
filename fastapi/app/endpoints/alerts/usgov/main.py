from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_usgov_alerts():
    return {"message": "US Government Alerts"}


@router.get("/{alert_id_usgov}/")
def get_usgov_alert(alert_id_usgov: str):
    return {"message": f"US Government Alert {alert_id_usgov}"}
