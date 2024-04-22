import requests
import json
from pymongo import MongoClient
from datetime import datetime
from BaseAPI import BaseAPI


class Event(BaseAPI):
    def __init__(self):
        self.gdacs_response = requests.get("https://www.gdacs.org/xml/rss.xml")
        self.usgs_response = requests.get(
            "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
        )
        self.client = MongoClient("mongodb://root:example@localhost:27017")
        self.db = self.client["events_db"]
        self.collection = self.db["events"]

    def get_event_data(self):
        gdacs_data = self._extract_gdacs_data()
        usgs_data = self._extract_usgs_data()

        combined_data = gdacs_data + usgs_data
        return combined_data

    def _extract_gdacs_data(self):
        if self.gdacs_response.status_code == 200:
            response_json = json.loads(self.gdacs_response.text)
            gdacs_data = []

            for item in response_json["rss"]["channel"]["item"]:
                geo_lat = item.get("geo_lat", None)
                geo_long = item.get("geo_long", None)
                published = item.get("published", None)

                gdacs_data.append(
                    {
                        "source": "GDACS",
                        "geo_lat": geo_lat,
                        "geo_long": geo_long,
                        "published": self._parse_date(published),
                    }
                )

            return gdacs_data
        else:
            print(
                "Failed to fetch GDACS data. Status code:",
                self.gdacs_response.status_code,
            )
            return []

    def _extract_usgs_data(self):
        if self.usgs_response.status_code == 200:
            response_json = self.usgs_response.json()
            usgs_data = []

            for feature in response_json["features"]:
                properties = feature["properties"]
                geometry = feature["geometry"]

                geo_lat = geometry["coordinates"][1]
                geo_long = geometry["coordinates"][0]
                published = properties["time"]

                usgs_data.append(
                    {
                        "source": "USGS",
                        "geo_lat": geo_lat,
                        "geo_long": geo_long,
                        "published": int(published / 1000),
                    }
                )

            return usgs_data
        else:
            print(
                "Failed to fetch USGS data. Status code:",
                self.usgs_response.status_code,
            )
            return []

    def _parse_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return int(date_obj.timestamp())

    def compare_and_store(self):
        event_data = self.get_event_data()

        for event in event_data:
            existing_event = self.collection.find_one(
                {
                    "source": event["source"],
                    "geo_lat": event["geo_lat"],
                    "geo_long": event["geo_long"],
                    "published": event["published"],
                }
            )
            if existing_event:
                print("Similar event already exists:", existing_event)
            else:
                self.collection.insert_one(event)
                print("New event inserted:", event)

    def getData(self):
        print("Work here")

    def getKeyOfId(self) -> str:
        pass

    def _collectData(self):
        pass
