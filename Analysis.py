import os
import time
from selenium import webdriver
import pymongo
import pandas as pd
import re
import folium
import io
from PIL import Image
from pandas import DataFrame

class Analysis:
    def __init__(self):
        self.type = ''
        self.year = ''
        self.kind = ''
        self.myClient = pymongo.MongoClient("mongodb://localhost:27017/")

    def setType(self, type):
        self.type = type

    def setYear(self, year):
        self.year = year

    def volumeAn(self):
        df = pd.DataFrame(list(self.collection.find(
            {'YEAR': int(self.year)})))
        cols = ['SECTION', 'GEOM', 'YEAR', 'SHAPE_LENGTH', 'TRAFFIC_VOLUME']
        droplist = [i for i in df.columns if i not in cols]
        df.drop(droplist, axis=1, inplace=True)
        df = df[cols]
        df_sum = self.dbSum(df,"SECTION","TRAFFIC_VOLUME")
        del df_sum["TRAFFIC_VOLUME"]
        return df_sum

    def incidentAn(self):
        df = pd.DataFrame(list(self.collection.find(
            {'START_DT': {'$regex': self.year}}
        )))
        cols = ['INCIDENT_INFO', 'DESCRIPTION', 'START_DT', 'MODIFIED_DT', 'QUADRANT', 'LONGITUDE', 'LATTITUDE',
                'LOCATION', 'COUNT']
        droplist = [i for i in df.columns if i not in cols]
        df.drop(droplist, axis=1, inplace=True)
        df = df[cols]
        df_sum = self.dbSum(df,"INCIDENT_INFO",'COUNT')
        del df_sum['COUNT']
        return df_sum

    def dbSum(self,df,key,count):
        df['TOTAL'] = df.groupby([key])[count].transform('sum')
        new_df = df.drop_duplicates(subset=[key])
        return new_df

    def read(self):
        dbName = "Volume_Incidents"
        word_list = self.type.split(' ')
        collectionName = str(word_list[0].lower()+self.year)
        self.db = self.myClient[dbName]
        self.collection = self.db[collectionName]
        if self.type == "Volume Analysis":
            vdf = self.volumeAn()
            return vdf

        elif self.type == "Incident Analysis":
            idf = self.incidentAn()
            return idf

    def sort(self,df):
        df_sorted = df.sort_values(by = ['TOTAL'], inplace = False, ascending = False)
        df_sorted = df_sorted.reset_index(drop = True)
        return df_sorted

    def maxperyear(self, year):
        self.setYear(year)
        df = self.read()
        total = int(df['TOTAL'].max())
        return total

    def mapPrep(self,df):
        self.m = folium.Map(location=[51.0447, -114.0719],tiles = 'OpenStreetMap',zoom_start=12)
        # finding coordinates
        self.maxvalue = self.maxperyear(self.year)
        max_df = df.loc[df['TOTAL']==self.maxvalue]
        self.drawMap(max_df)




    def drawMap(self,df):
        for index, row in df.iterrows():
            location =[0]*2
            if self.type == "Incident Analysis":
                location[0] = df.iloc[index,6]
                location[1] = df.iloc[index,5]
                folium.Marker(location = location,color="blue").add_to(self.m)
            elif self.type == "Volume Analysis":
                line = df.iloc[index,1]
                newline =re.sub('[^-0-9,\\s.]','',line)
                points = []
                string_points = newline.strip().split(',')
                for pairs in string_points:
                    string_pair = pairs.strip().split(' ')
                    for i in range(len(string_pair)):
                        string_pair[i] = float(string_pair[i])
                    points.append(tuple(reversed(string_pair)))

                folium.PolyLine(points, color = "blue", weight = 4, opacity =1).add_to(self.m)

        # Generate map
        delay  = 1
        fn = 'Map.html'
        tmpurl = 'file:///Users/thiennguyen/Desktop/ENSF592/Project/ENSF592-Project/{mapfile}'.format(path=os.getcwd(), mapfile = fn)
        self.m.save(fn)
        browser = webdriver.Chrome()
        browser.get(tmpurl)
        time.sleep(delay)
        browser.save_screenshot('Map.png')
        browser.quit()

        im = Image.open('Map.png')
        im = im.convert('RGB').convert('P', palette = Image.ADAPTIVE)
        im.save('Map.gif')















