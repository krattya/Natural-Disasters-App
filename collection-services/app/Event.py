import logging
from pymongo import MongoClient
from typing import List
from BaseAPI import BaseAPI


class Event(BaseAPI):
    _id_key = "id"

    logging.basicConfig(level=logging.INFO)

    def __init__(self, db) -> None:
        super().__init__(db["events"])
        self.logger = logging.getLogger(__name__)

    def getData(self) -> List:
        data = self._collectData()
        if data:
            for event_id, event_data in data.items():
                self.logger.info("Checking event:", event_data)
                if not self.db_collection_manager.event_exists(event_id, self._id_key):
                    self.logger.info("Saving event:", event_data)
                    self._save_data(event_data)
                else:
                    self.logger.info(
                        f"Event with ID {event_id} already exists in the database."
                    )
        else:
            self.logger.info("No events to save.")

    def getKeyOfId(self) -> str:
        return self._id_key

    def _collectData(self):
        self.logger.info("Fetching data from the database...")

        # Connect to MongoDB
        db_connect = MongoClient("mongodb://root:example@mongo:27017/")
        db = db_connect["disaster_information"]
        gdacs_collection = db["gdacs_events"]
        usgs_collection = db["usgov_events"]

        # Retrieve data from MongoDB
        gdacs_data = gdacs_collection.find({"source": "gdacs_events"})
        usgs_data = usgs_collection.find({"source": "usgov_events"})

        # Initialize dictionary to store combined data
        combined_data = {}

        # Parse GDACS data
        for event in gdacs_data:
            event_id = event.get("id")
            if event_id is not None:
                if event_id not in combined_data:
                    key = (
                        event.get("published"),
                        event.get("geo_lat"),
                        event.get("geo_long"),
                    )
                    combined_data[event_id] = {"key": key, "data": event}
                else:
                    existing_event = combined_data[event_id]["data"]
                    existing_event.update(event)

        # Parse USGS data
        for event in usgs_data:
            event_id = event.get("id")
            if event_id is not None:
                if event_id not in combined_data:
                    key = (
                        event.get("properties", {}).get("time"),
                        event.get("geometry", {}).get("coordinates", [])[1],
                        event.get("geometry", {}).get("coordinates", [])[0],
                    )
                    combined_data[event_id] = {"key": key, "data": event}
                else:
                    existing_event = combined_data[event_id]["data"]
                    existing_event.update(event)

        return combined_data if combined_data else None
