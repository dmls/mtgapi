import pymongo
from pymongo import MongoClient

class DB:
    def __init__(self, uri = 'mongodb://localhost:27017', db_name = 'mtgapi'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
