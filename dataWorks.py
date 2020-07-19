import json
import pymongo
import pandas as pd


class dataWorks:
    def __init__(self, dbName, collectionName):
        self.myClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.myClient[dbName]
        self.collection = self.db[collectionName]
        self.collection.create_index("id", unique=True)

    def Csv_to_DB(self, filename, encoding, new_filename):
        df = pd.read_csv(filename, encoding=encoding)
        df.to_json(new_filename, orient="records")
        jdf = open(new_filename).read()
        data = json.loads(jdf)
        self.collection.insert_many(data)


