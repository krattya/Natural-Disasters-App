from abc import abstractmethod, ABC
from typing import List, Any
from DatabaseManager import DatabaseManager


class BaseAPI(ABC):
    def __init__(self, db_collection) -> None:
        self.db_collection_manager = DatabaseManager(db_collection)

    def _save_data(self, alert: Any):
        print("Saving data:", alert)
        self.db_collection_manager.add_event(alert)

    @abstractmethod
    def getData(self) -> List:
        pass

    @abstractmethod
    def getKeyOfId(self) -> str:
        pass

    @abstractmethod
    def _collectData(self):
        pass
