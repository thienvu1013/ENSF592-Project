import json
import pymongo
import pandas as pd


class dataWorks:
    def __init__(self, dbName, collectionName):
        self.myClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.myClient[dbName]
        self.collection = self.db[collectionName]

    def Csv_to_DB(self, filename, encoding, new_filename):
        df = pd.read_csv(filename, encoding=encoding)
        column_names = df.columns.tolist()
        new_column = []

        if "volume" in new_filename:
            for name in column_names:
                new_name = ""
                lower_name = name.lower()
                if "year" in lower_name:
                    new_name = "year"
                elif "name" in lower_name:
                    new_name = "section"
                elif "len" in lower_name:
                    new_name = "shape_length"
                elif "volume" in lower_name:
                    new_name = "traffic_volume"
                else:
                    new_name = "geom"
                new_column.append(new_name.upper())
            df.columns = new_column

        if "incident" in new_filename:
            for name in column_names:
                new_name = ""
                lower_name = name.lower()
                if "incident" in lower_name:
                    new_name = "incident_info"
                elif "description" in lower_name:
                    new_name = "description"
                elif "start" in lower_name:
                    new_name = "start_dt"
                elif "modified" in lower_name:
                    new_name = "modified_dt"
                elif "quadrant" in lower_name:
                    new_name = "quadrant"
                elif "long" in lower_name:
                    new_name = "longitude"
                elif "lat" in lower_name:
                    new_name = "lattitude"
                elif "loc" in lower_name:
                    new_name = "location"
                elif "count" in lower_name:
                    new_name = "count"
                else:
                    new_name = "id"
                new_column.append(new_name.upper())
            df.columns = new_column

        df.to_json(new_filename, orient="records")
        jdf = open(new_filename).read()
        data = json.loads(jdf)
        self.collection.insert_many(data)

'''
volume2016 = dataWorks('Volume_Incidents', "volume2016")
volume2016.Csv_to_DB("TrafficFlow2016_OpenData.csv","ASCII","volume2016.json")
volume2017 = dataWorks('Volume_Incidents', "volume2017")
volume2017.Csv_to_DB("2017_Traffic_Volume_Flow.csv","ASCII","volume2017.json")
volume2018 = dataWorks('Volume_Incidents', "volume2018")
volume2018.Csv_to_DB("Traffic_Volumes_for_2018.csv","ASCII","volume2018.json")
incident2016 = dataWorks('Volume_Incidents', "incident2016")
incident2016.Csv_to_DB("Traffic_Incidents_Archive_2016.csv","ASCII","incident2016.json")
incident2017 = dataWorks('Volume_Incidents', "incident2017")
incident2017.Csv_to_DB("Traffic_Incidents_Archive_2017.csv","ASCII","incident2017.json")
incident2018 = dataWorks('Volume_Incidents', "incident2018")
incident2018.Csv_to_DB("Traffic_Incidents.csv","ASCII","incident2018.json")
'''

