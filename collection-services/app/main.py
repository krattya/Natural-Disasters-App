import gdacs.api as gdacs_api
from pymongo import MongoClient
from model import MainAlerts
import time

client = MongoClient("mongodb://root:example@mongo:27017/")
db = client["disaster_information"]
collection_gdac_events = db["gdacs_events"]
collection_main_events = db["main_events"]


def main_event_exists_for_gdac_event(gdac_event):
    return collection_main_events.find_one({"gdac_id": gdac_event["id"]}) is not None


def add_new_main_event(gdac_event_id=None):
    newEvent = MainAlerts(gdac_id=gdac_event_id)
    # TODO: Find event that matches
    collection_main_events.insert_one(newEvent.model_dump())


def add_event_to_db(events, collection, idKey="id"):
    for event in events:
        # print(event)
        if collection.find_one({"id": event[idKey]}) is None:
            print(f"Inserting event {event[idKey]} into the database...")
            collection.insert_one(event)
            if main_event_exists_for_gdac_event(event):
                print(
                    f"Event {event[idKey]} already exists in the main event collection... Skipping..."
                )
            else:
                print(
                    f"Event {event[idKey]} does not exist in the main event collection... Adding the event..."
                )
                add_new_main_event(gdac_event_id=event["id"])
        else:
            print(
                f"Event {event[idKey]} already exists in the database... Updating the event..."
            )
            collection.delete_one({"id": event[idKey]})
            collection.insert_one(event)


def main():
    print("[x] Starting the collection services...")
    while True:
        print("[x] Fetching data from GDACS...")
        events = gdacs_api.get_all_alerts()
        add_event_to_db(events, collection_gdac_events)
        time.sleep(120)


if __name__ == "__main__":
    main()
