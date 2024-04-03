import gdacs.api as gdacs_api
from pymongo import MongoClient
from model import MainAlerts

client = MongoClient(
    "mongodb://root:example@mongo:27017/"
)  # Replace with your connection URI
db = client["disaster_information"]
collection_gdac_events = db["gdacs_events"]
collection_main_events = db["main_events"]


def main_event_exists_for_gdac_event(gdac_event):
    return collection_main_events.find_one({"gdac_id": gdac_event["id"]}) is not None


def add_new_main_event(gdac_event_id=None):
    newEvent = MainAlerts(gdac_id=gdac_event_id)
    # TODO: Find event that matches
    collection_main_events.insert_one(newEvent.model_dump())


def add_event_to_db(events, collection):
    for event in events:
        # print(event)
        if collection.find_one({"id": event["id"]}) is None:
            print(f"Inserting event {event['id']} into the database...")
            collection.insert_one(event)
            if main_event_exists_for_gdac_event(event):
                print(
                    f"Event {event['id']} already exists in the main event collection... Skipping..."
                )
            else:
                print(
                    f"Event {event['id']} does not exist in the main event collection... Adding the event..."
                )
                add_new_main_event(gdac_event_id=event["id"])
        else:
            print(
                f"Event {event['id']} already exists in the database... Updating the event..."
            )
            collection.delete_one({"id": event["id"]})
            collection.insert_one(event)


def main():
    print("[x] Starting the collection services...")
    events = gdacs_api.get_all_alerts()
    add_event_to_db(events, collection_gdac_events)


if __name__ == "__main__":
    main()
