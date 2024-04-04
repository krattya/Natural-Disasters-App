from fastapi import Request, HTTPException, status


def get_all_gdacs_alerts(request: Request):
    return list(request.app.db["gdacs_events"].find({}, {"_id": 0}))


def get_gdacs_alert(alert_id_gdac: str, request: Request):
    data = request.app.db["gdacs_events"].find_one({"id": alert_id_gdac}, {"_id": 0})
    if data:
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id_gdac} not found",
        )
