import logging
from pymongo import MongoClient
from typing import List
from BaseAPI import BaseAPI
from pydantic import BaseModel
import time


class Event_Mod(BaseModel):
    gdacs_id: str
    usgov_id: str
    last_updated: float = None


class Event(BaseAPI):
    _id_key = "id"
    _db_db = None
    log = None

    def __init__(self, db) -> None:
        super().__init__(db["events"])
        db_connect = MongoClient("mongodb://root:example@mongo:27017/")
        self._db_db = db_connect["disaster_information"]
        self.log = logging.getLogger()

    def pase_gdacs_time(self, gdacs_time):
        return time.time()

    def event_match(self, gdac, usgov) -> bool:
        return True

        # unix time to python time
        # usgov_time = time.gmtime(usgov["properties"]["time"] / 1000)
        # print(f"gdac_time: {usgov_time}")
        # gdacs_info_with_event_time = self.pase_gdacs_time(gdac["summary"])
        # gdacs_time = self.pase_gdacs_time(gdacs_info_with_event_time)

        # if abs(gdacs_time - usgov["properties"]["time"]) <= 500:
        #    return True
        # else:
        #    return False

    def is_event_exists(self, key, id) -> bool:
        event = self._db_db["events"].find_one({key: id})
        if event is None:
            return False
        return True

    def is_new_event_to_db(self, event: Event_Mod) -> bool:
        if self.is_event_exists("gdacs_id", event.gdacs_id) and self.is_event_exists(
            "usgov_id", event.usgov_id
        ):
            return False
        return True

    def getData(self) -> List:
        all_gdacs = self._db_db["gdacs_events"].find({})
        all_usgov = self._db_db["usgov_events"].find({})

        for gdac in all_gdacs:
            for usgov in all_usgov:
                if self.event_match(gdac, usgov):
                    self.log.info(f"Event matched: {gdac['id']} {usgov['id']}")
                    event = Event_Mod(
                        gdacs_id=gdac["id"],
                        usgov_id=usgov["id"],
                        last_updated=time.time(),
                    )
                    json_event = event.model_dump()
                    if self.is_new_event_to_db(event):
                        result = self._db_db["events"].insert_one(json_event)
                        print(
                            f"New event added: {result.inserted_id} gdacs_id:  {event.gdacs_id}  usgov_id: {event.usgov_id}"
                        )

    def _collectData(self):
        pass
