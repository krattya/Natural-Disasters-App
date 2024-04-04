import gdacs.api as gdacs_api
from pymongo import MongoClient
from model import MainAlerts
import time

class DatabaseManager:
    def __init__(self, collection):
        self.collection = collection

    def event_exists(self, event_id):
        return self.collection.find_one({"id": event_id}) is not None

    def add_event(self, event):
        self.collection.insert_one(event)

    def update_event(self, event_id, event):
        self.collection.delete_one({"id": event_id})
        self.collection.insert_one(event)

class EventManager:
    def __init__(self, gdacs_collection, main_events_collection):
        self.gdacs_db = DatabaseManager(gdacs_collection)
        self.main_events_db = DatabaseManager(main_events_collection)

    def add_new_main_event(self, gdac_event_id=None):
        newEvent = MainAlerts(gdac_id=gdac_event_id)
        self.main_events_db.add_event(newEvent.model_dump())

    def add_event_to_db(self, events):
        for event in events:
            event_id = event["id"]
            if not self.gdacs_db.event_exists(event_id):
                print(f"Inserting event {event_id} into the database...")
                self.gdacs_db.add_event(event)
                if self.main_events_db.event_exists(event_id):
                    print(f"Event {event_id} already exists in the main event collection... Skipping...")
                else:
                    print(f"Event {event_id} does not exist in the main event collection... Adding the event...")
                    self.add_new_main_event(gdac_event_id=event_id)
            else:
                print(f"Event {event_id} already exists in the database... Updating the event...")
                self.gdacs_db.update_event(event_id, event)

    def start_collection_services(self):
        print("[x] Starting the collection services...")
        while True:
            print("[x] Fetching data from GDACS...")
            events = gdacs_api.get_all_alerts()
            self.add_event_to_db(events)
            time.sleep(120)

if __name__ == "__main__":
    client = MongoClient("mongodb://root:example@mongo:27017/")
    db = client["disaster_information"]
    collection_gdac_events = db["gdacs_events"]
    collection_main_events = db["main_events"]
    event_manager = EventManager(collection_gdac_events, collection_main_events)
    event_manager.start_collection_services()