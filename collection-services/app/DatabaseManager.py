class DatabaseManager:
    def __init__(self, collection):
        self.collection = collection

    def event_exists(self, event_id, key):
        event = self.collection.find_one({key: event_id})
        return event is not None

    def add_event(self, event):
        self.collection.insert_one(event)

    def update_event(self, event_id, new_event_data, key):
        existing_event = self.collection.find_one({key: event_id})
        if existing_event:
            self.collection.update_one({key: event_id}, {"$set": new_event_data})
        else:
            self.collection.insert_one(new_event_data)

    def get_all_events(self):
        return self.collection.find()

    def get_events_by_source(self, source):
        return self.collection.find({"source": source})

    def save_event(self, event):
        self.collection.insert_one(event)
