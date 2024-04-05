class DatabaseManager:
    def __init__(self, collection):
        self.collection = collection

    def event_exists(self, event_id, key):
        return self.collection.find_one({key: event_id}) is not None

    def add_event(self, event):
        self.collection.insert_one(event)

    def update_event(self, event_id, event, key):
        # TODO: Implement update event
        # check if event exists
        # check if event is different -> update
        self.collection.delete_one({key: event_id})
        self.collection.insert_one(event)
