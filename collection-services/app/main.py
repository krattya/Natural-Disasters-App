from typing import List
from BaseAPI import BaseAPI
from usgov import USGOV
from pymongo import MongoClient
import time

db_connect = MongoClient("mongodb://localhost:27017/")
db = db_connect["disaster_information"]


dataCollectors: List[BaseAPI] = [USGOV(db=db)]


def main():
    while True:
        for collector in dataCollectors:
            print(collector.getData())

        time.sleep(10000)


if __name__ == "__main__":
    main()
