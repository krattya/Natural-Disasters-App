from app.endpoints.alerts.models import AlertInDB
from typing import List
from fastapi import HTTPException


def get_all_alerts(db) -> List[AlertInDB]:
    return db["alerts"].find({})


def get_alert_by_id(alert_id: str, db):
    data = db["alerts"].find_one({"id": alert_id}, {"_id": 0})
    if data:
        return data
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found",
        )
