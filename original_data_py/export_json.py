#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import json

#url = 'https://suitable-house-default-rtdb.firebaseio.com/'

Data1 = pd.read_csv('Realtor_info.csv')
Data2 = pd.read_csv('School_location.csv')
Data3 = pd.read_csv('Crime_info.csv')


# In[3]:


with open('Realtor_info.json', 'w') as f:
    f.write(Data1.to_json(orient='records'))
with open('School_location.json', 'w') as f:
    f.write(Data2.to_json(orient='records'))
with open('Crime_info.json', 'w') as f:
    f.write(Data3.to_json(orient='records'))


# In[33]:


f1 = open('data/Crime_info.json', "r") 
f2 = open('data/Realtor_info.json', "r") 
f3 = open('data/School_location.json', "r") 

data1 = json.load(f1)
data2 = json.load(f2)
data3 = json.load(f3)
data_1 = {}
data_1['Crime'] = data1
data_1['Realtor'] = data2
data_1['School'] = data3

f1.close()
f2.close()
f3.close()

with open('data/combine_data.json', 'w') as outfile:
    json.dump(data_1, outfile)


# In[ ]:




