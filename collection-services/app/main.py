import gdacs.api as gdacs_api
import usgov.api as usgov_api
from pymongo import MongoClient
from model import MainAlerts
import time


class DatabaseManager:
    def __init__(self, collection):
        self.collection = collection

    def event_exists(self, event_id, key):
        return self.collection.find_one({key: event_id}) is not None

    def add_event(self, event):
        self.collection.insert_one(event)

    def update_event(self, event_id, event, key):
        self.collection.delete_one({key: event_id})
        self.collection.insert_one(event)


class EventManager:
    def __init__(self, db):
        self.gdacs_db = DatabaseManager(db["gdacs_events"])
        self.usgov_db = DatabaseManager(db["usgov_events"])
        self.main_events_db = DatabaseManager(db["main_events"])

    def start_collection_services(self):
        print("[x] Starting the collection services...")


class EventManager1:
    def __init__(self, db):
        self.gdacs_db = DatabaseManager(db["gdacs_events"])
        self.usgov_db = DatabaseManager(db["usgov_events"])
        self.main_events_db = DatabaseManager(db["main_events"])

    def add_new_main_event(self, gdac_event_id=None, usgov_event_id=None):
        newEvent = MainAlerts(gdac_id=gdac_event_id)
        self.main_events_db.add_event(newEvent.model_dump())

    def add_event_to_db(self, events, key, event_collection: DatabaseManager):
        for event in events:
            event_id = event[key]
            if not self.gdacs_db.event_exists(event_id):
                print(f"Inserting event {event_id} into the database...")
                self.gdacs_db.add_event(event)
                if self.main_events_db.event_exists(event_id):
                    print(
                        f"Event {event_id} already exists in the main event collection... Skipping..."
                    )
                else:
                    print(
                        f"Event {event_id} does not exist in the main event collection... Adding the event..."
                    )
                    self.add_new_main_event(gdac_event_id=event_id)
            else:
                print(
                    f"Event {event_id} already exists in the database... Updating the event..."
                )
                self.gdacs_db.update_event(event_id, event)

    def handle_usgov_event(self, event):
        print("[x] Fetching data from USGOV...")
        events = usgov_api.get_all_alerts()
        self.add_event_to_db(events, "id")

    def handle_gdacs_event(self, event):
        print("[x] Fetching data from GDACS...")
        events = gdacs_api.get_all_alerts()
        self.add_event_to_db(events, "id")

    def start_collection_services(self):
        print("[x] Starting the collection services...")
        while True:
            self.handle_gdacs_event()
            self.handle_usgov_event()
            time.sleep(10020)


if __name__ == "__main__":
    client = MongoClient("mongodb://root:example@mongo:27017/")
    db = client["disaster_information"]
    event_manager = EventManager(db)
    event_manager.start_collection_services()
