import logging
from pymongo import MongoClient
from typing import List
from BaseAPI import BaseAPI
from pydantic import BaseModel


class Event_Mod(BaseModel):
    gdacs_id: str
    usgov_id: str


class Event(BaseAPI):
    _id_key = "id"
    _db_db = None

    def __init__(self, db) -> None:
        super().__init__(db["events"])
        db_connect = MongoClient("mongodb://root:example@mongo:27017/")
        self._db_db = db_connect["disaster_information"]

    def event_match(self, data1, data2):
        return True

    def getData(self) -> List:
        print("[x] Creating events from matched data")
        all_gdacs = self._db_db["gdacs_events"].find({})
        all_usgov = self._db_db["usgov_events"].find({})

        for gdac in all_gdacs:
            for usgov in all_usgov:
                if self.event_macht(gdac, usgov):
                    event = Event_Mod(gdacs_id=gdac["id"], usgov_id=usgov["id"])
                    json_event = event.model_dump()
                    logging.info(f"Event matched: {json_event}")
                    result = self._db_db["events"].insert_one(json_event)
                    print(f"Event matched insert id: {result.inserted_id}")

    def _collectData(self):
        pass
