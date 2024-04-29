from fastapi import Request, HTTPException, status


def get_all_usgov_alerts(request: Request):
    return list(request.app.db["usgov_events"].find({}, {"_id": 0})).limit(1000)


def get_usgov_alert(alert_id_usgov: str, request: Request):
    data = request.app.db["usgov_events"].find_one({"id": alert_id_usgov}, {"_id": 0})
    if data:
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id_usgov} not found",
        )
