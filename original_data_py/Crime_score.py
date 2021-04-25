#!/usr/bin/env python
# coding: utf-8

# In[61]:


import requests
from bs4 import BeautifulSoup 
from pprint import pprint
import pandas as pd

url = "https://www.neighborhoodscout.com/blog/top100dangerous"
response = requests.request("GET", url)
soup = BeautifulSoup(response.content, 'lxml')
location = soup.find('div', {'class' : 'entry-content'})
every_location= location.findAll('h3')
city = []
state = []
for i in every_location:#.findAll('a'):
    cs = i.find('a').text.split(',')
    city.append(cs[0].strip())
    state.append(cs[1].strip())
crime_rate = []
chance_crime = []
crime = soup.findAll('ul', {'style' : 'list-style-type: circle;'})
for i in crime:
    for j in range(len(i.findAll('li'))):
        if j == 0 :
            crime_rate.append(i.findAll('li')[j].text.split(':')[1].strip())
        else:
            chance_crime.append(i.findAll('li')[j].text.split(':')[1].strip())

whole_crime = [city, state, crime_rate, chance_crime]
Crime_info = {'city': [],'state':[], 'crime_rate': [], 'chance_crime': []}
for i in range(len(whole_crime[0])):
    Crime_info['city'].append(whole_crime[0][i])
    Crime_info['state'].append(whole_crime[1][i])
    Crime_info['crime_rate'].append(whole_crime[2][i])
    Crime_info['chance_crime'].append(whole_crime[3][i])
Crime_info_df = pd.DataFrame(Crime_info)


# In[62]:


Crime_info_df.to_csv("data/Crime_info.csv", index=False, sep=',')


# In[ ]:




