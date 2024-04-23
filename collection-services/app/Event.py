import requests
import json
from pymongo import MongoClient
from datetime import datetime
from BaseAPI import BaseAPI
import feedparser


class Event(BaseAPI):
    _id_key = "id"

    def __init__(self):
        super().__init__()
        self.client= MongoClient("mongodb://root:example@mongo:27018/")
        self.db = ["events_db"]

    def getData(self):
        print("[x]Fetching data from GDACS and USGS APIs...")
        event_list = self.get_event_data()

        for event in event_list:
            if not self.is_event_duplicate(event):
                self.db_collection_manager.save_event(event)
                print("New event inserted:", json.dumps(event))
            else:
                print("Event already exists:", json.dumps(event))
        
        return event_list

    def getKeyOfId(self) -> str:
        return self._id_key

    def is_event_duplicate(self, event):
        existing_event = self.db_collection_manager.find_event(
            {
                "geo_lat" : event["geo_lat"],
                "geo_long" : event["geo_long"],
                "published" : event["published"],
            }
        )
        return existing_event is not None

    def _collectData(self):
        print("Fetching data from GDACS and USGS APIs...")
        gdacs_data = self._collect_gdacs_data()
        usgs_data = self._collect_usgs_data()

        print("GDACS data lenght:", len(gdacs_data))
        print("USGS data lenght:", len(usgs_data))


        combined_data = self._collect_gdacs_data + self._collect_usgs_data
        return combined_data

    def _collect_gdacs_data(self):
        print ("[x] Fetching data from GDACS RSS Feed")
        gdacs_feed = feedparser.parse("https://www.gdacs.org/xml/rss.xml")

        events = gdacs_feed.entries
        gdacs_data = []

        for event in events:
            geo_lat = event.get("geo_lat", None)
            geo_long = event.get("geo_long", None)
            published = event.get("published", None)
            event_id = event.get("id", None)

            gdacs_data.append(
                {
                    self._id_key: event_id,
                    "source": "GDACS",
                    "geo_lat": geo_lat,
                    "geo_long": geo_long,
                    "published": self._parse_date(published),
                }
            )
        return gdacs_data
        
    def _collect_usgs_data(self):
        print ("[x] Fetching data from USGS")
        response = requests.get(
            "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
            )
        data = response.json()
        usgs_events = data.get("features", [])

        usgs_data = []

        for event in usgs_events:
            properties = event.get("properties", [])
            geometry = event.get("geometry", [])

            geo_lat = geometry.get("coordinates", [][1])
            geo_long = geometry.get("coordinates", [][0])
            published = properties.get("time", None)
            event_id = properties.get("id", None)

            usgs_data.append(
                {
                    self._id_key: event_id,
                    "source": "USGS",
                    "geo_lat": geo_lat,
                    "geo_long": geo_long,
                    "published": int(published / 1000),
                }
            )
        return usgs_data
    
    def _parse_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return int (date_obj.timestamp())