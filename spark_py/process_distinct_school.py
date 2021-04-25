#!/usr/bin/env python
# coding: utf-8

# In[40]:


import math
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
import pyspark.sql.functions as fc
import json
import requests

spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("readCSV").getOrCreate()
Data = spark.read.csv('Realtor_info.csv', header=True)
Data1 = spark.read.csv('School_location1.csv', header=True)

Data = Data.toPandas()
Data1 = Data1.toPandas()

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d
Data = Data.dropna()
Data = Data.reset_index(drop=True)


# In[41]:


Data['Avg_sqft(PCode)'] = np.nan
postal_codes = Data['postal_code'].tolist()
postal_codes = list(set(postal_codes))
for postal in postal_codes:
    postal_values = Data[Data['postal_code'] == postal]
    sqfts = postal_values['sqft'].tolist()
    sqfts1 = []
    for i in sqfts:
        try:
            s = int(''.join(filter(str.isdigit,i)))
        except:
            s = 0
        sqfts1.append(s) 
    if len(sqfts1) !=0 :
        avg = sum(sqfts1)/len(sqfts1)
    Data['Avg_sqft(PCode)'].loc[postal_values.index] = avg


# In[46]:


Distance = []
School = []
for i in range(len(Data)):
    distance1 = []
    school1 = []
    for j in range(len(Data1)):
        if Data['city'][i] == Data1['CITY'][j]:
            lat1 = (float(Data['lat'][i]),float((Data['lon'][i])))
            lat2 = (float(Data1['LAT'][j]),float((Data1['LON'][j])))
            dist = round(distance(lat1, lat2), 1)
            distance1.append(dist)
            school1.append(Data1['NAME'][j])
        else:
            continue
    if len(distance1) !=0:
        Distance.append(max(distance1))
        School.append(school1[distance1.index(max(distance1))])
    else:
        Distance.append(10000)
        School.append('No-school')


# In[45]:


'''
Distance_1 = Distance
School_1 = School
print(Distance_1)
print(School_1)
Distance_1.extend(Distance)
School_1.extend(School)
'''


# In[49]:


school_distinct = []
for i in Distance:
    if i < 10:
        school_distinct.append('Yes')
    else:
        school_distinct.append('No')


# In[50]:


Data['School_district'] = school_distinct
Data['Nearly_school'] = School


# In[59]:


Data['Avg_price(PCode)'] = np.nan
postal_codes = Data['postal_code'].tolist()
for postal in postal_codes:
    postal_values = Data[Data['postal_code'] == postal]
    prices = postal_values['price'].tolist()
    prices1 = []
    for j in prices:
        try:
            p = int(''.join(filter(str.isdigit,j)))
        except:
            p = 0
        prices1.append(p) 
    if len(prices1) !=0 :
        avg1 = sum(prices1)/len(prices1)
    Data['Avg_price(PCode)'].loc[postal_values.index] = avg1


# In[61]:


Data.to_csv("Realtor_info1.csv", index=False, sep=',')
with open('Realtor_info1.json', 'w') as f:
    f.write(Data.to_json(orient='records'))


# In[62]:


result = Data.to_json(orient="records")
parsed = json.loads(result)
data = json.dumps(parsed)
url = 'https://house-9f5c0-default-rtdb.firebaseio.com/Realtor.json'
response = requests.put(url,data)


# In[58]:




