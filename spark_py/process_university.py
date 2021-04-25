#!/usr/bin/env python
# coding: utf-8

# In[37]:


from pyspark.sql import SparkSession
import pyspark.sql.functions as fc
import json
import requests

spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("readCSV").getOrCreate()
Data = spark.read.csv('Realtor_info.csv', header=True)
Data1 = spark.read.csv('School_location.csv', header=True)
df = Data.toPandas()
df1 = Data1.toPandas()
city = df['city'].tolist()
City = []
for i in city:
    if i in City:
        continue
    else:
        City.append(i)
for i in range(len(df1['CITY'])): 
    if df1['CITY'][i] in City:
        continue
    else:
        df1 = df1.drop(i)
df1 = df1.reset_index(drop=True)
df1.to_csv("School_location1.csv", index=False, sep=',')
with open('School_location1.json', 'w') as f:
    f.write(df1.to_json(orient='records'))  
file = open('School_location1.json',)
json1= json.load(file)
url = 'https://house-9f5c0-default-rtdb.firebaseio.com/School.json'
response = requests.put(url,json = json1)

