from typing import List
from BaseAPI import BaseAPI
from usgov import USGOV
from gdacs import GDACS
from pymongo import MongoClient
import time
from Event import Event

db_connect = MongoClient("mongodb://root:example@mongo:27017/")
db = db_connect["disaster_information"]


dataCollectors: List[BaseAPI] = [USGOV(db=db), GDACS(db=db), Event(db=db)]


def main():
    while True:
        for collector in dataCollectors:
            print(f"[x] Collecting data from {collector.__class__.__name__}")
            collector.getData()

        print("[x] Sleeping for 10 seconds")
        time.sleep(10)


if __name__ == "__main__":
    main()
