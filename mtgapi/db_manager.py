import pymongo
from pymongo import MongoClient

class DBManager:
    def __init__(self, uri = 'mongodb://localhost:27017', db_name = 'mtgapi'):
        client = MongoClient(uri)
        self.db = client[db_name]
