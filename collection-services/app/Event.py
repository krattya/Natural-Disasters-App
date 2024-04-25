import requests
import json
from datetime import datetime
from typing import List
from BaseAPI import BaseAPI
import feedparser
import uuid

class Event(BaseAPI):
    _id_key = "id"
    
    def __init__(self, db) -> None:
        super().__init__(db["events"])


    def getData(self) -> List:
        alert_list = self.db_collection_manager.get_all_events()

        for alert in alert_list:
            if not self.db_collection_manager.event_exists(alert[self._id_key], self._id_key):
                self._save_data(alert)
        else:
            self.db_collection_manager.update_event(alert[self._id_key], alert, self._id_key)
    
        json_data = json.dumps(alert_list)
        return json_data
        
    def generate_unique_id(self):
        return str(uuid.uuid4())
    
    def getKeyOfId(self) -> str:
        return self._id_key
    
    def _collectData(self):
        print("Fetching data from the database...")
    
    # Retrieve data from the database for both GDACS and USGS
        gdacs_data = self.db_collection_manager.get_events_by_source("GDACS")
        usgs_data = self.db_collection_manager.get_events_by_source("USGS")


    # Parse data from GDACS
        gdacs_parsed_data = []
        for event in gdacs_data:
            gdacs_parsed_data.append({
            "time": event["published"],
            "geo_lat": event["geo_lat"],
            "geo_long": event["geo_long"]
        })

    # Parse data from USGS
        usgs_parsed_data = []
        for event in usgs_data:
            usgs_parsed_data.append({
            "time": event["properties"]["time"],
            "geo_lat": event["geometry"]["coordinates"][1],
            "geo_long": event["geometry"]["coordinates"][0]
        })

    # Compare data from both sources
        for gdacs_event in gdacs_parsed_data:
            for usgs_event in usgs_parsed_data:
                if (gdacs_event["time"] == usgs_event["time"] and
                gdacs_event["geo_lat"] == usgs_event["geo_lat"] and
                gdacs_event["geo_long"] == usgs_event["geo_long"]):
                    new_event = {
                    "_id": self.generate_unique_id(),  
                    "time": gdacs_event["time"],
                    "geo_lat": gdacs_event["geo_lat"],
                  "geo_long": gdacs_event["geo_long"]
                }
                self.db_collection_manager.save_event(new_event)
    



        