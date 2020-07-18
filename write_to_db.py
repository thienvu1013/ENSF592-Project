import json
import pymongo
import pandas as pd

class write2db:
    def __init__(self, filename, encoding, new_filename, collectionName):
        myclient = pymongo.MongoClient("mongodb+srv://thienvu1013:Ohohoh123@cluster0.0mzux.mongodb.net/<dbname>?retryWrites=true&w=majority")
        df = pd.read_csv(filename, encoding = encoding)
        df.to_json(new_filename, orient="records")
        jdf = open(new_filename).read()
        data = json.loads(jdf)
        db = myclient["Traffic_and_Accident"]
        collection = db[collectionName]
        collection.insert_many(data)


write2db("Traffic_Incidents.csv", "ASCII", "Incident.json", "Incidents")

