from BaseAPI import BaseAPI
from typing import List
import requests


class USGOV(BaseAPI):
    _id_key = "id"

    def __init__(self, db) -> None:
        super().__init__(db["usgov_events"])

    def getData(self) -> List:
        alert_list = self._collectData()["features"]

        for alert in alert_list:
            if not self.db_collection_manager.event_exists(
                alert[self._id_key], self._id_key
            ):
                self._save_data(alert)
            else:
                self.db_collection_manager.update_event(
                    alert[self._id_key], alert, self._id_key
                )

        return alert_list

    def getKeyOfId(self) -> str:
        return self._id_key

    def _collectData(self):
        response = requests.get(
            "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
        )
        data = response.json()
        return data
