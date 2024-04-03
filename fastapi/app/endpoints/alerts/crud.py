from app.endpoints.alerts.models import AlertInDB
from typing import List


def get_all_alerts(db) -> List[AlertInDB]:
    return db["alerts"].find({})
