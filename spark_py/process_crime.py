#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession
import pyspark.sql.functions as fc
import json
import requests

spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("readCSV").getOrCreate()
Data = spark.read.csv('Crime_info.csv', header=True)
df = Data.toPandas()
with open('Crime_info1.json', 'w') as f:
    f.write(df.to_json(orient='records'))  
file = open('Crime_info1.json',)
json1= json.load(file)
url = 'https://house-9f5c0-default-rtdb.firebaseio.com/Crime.json'
response = requests.put(url,json = json1)

