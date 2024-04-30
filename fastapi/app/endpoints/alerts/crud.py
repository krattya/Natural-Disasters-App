from typing import List, Any
from fastapi import HTTPException


def get_all_alerts(db) -> List[Any]:
    return db["events"].find({}, {"_id": 0}).limit(1000).sort({"last_updated": -1})


def get_alert_by_id(alert_id: str, db):
    data = db["events"].find_one({"id": alert_id}, {"_id": 0})
    if data:
        return data
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found",
        )
