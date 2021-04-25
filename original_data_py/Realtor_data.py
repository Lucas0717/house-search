#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup 
from pprint import pprint
import requests
import pandas as pd
import numpy as np

# get all states and their Abbreviation
url_state_code = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States'
rq_1 = requests.get(url_state_code)
soup_1 = BeautifulSoup(rq_1.content, 'lxml')
state_code = soup_1.findAll('table')[0].findAll('tr')
state = []
state_abb = []
for i in range(2,len(state_code)):
    state.append(state_code[i].find('a').text)
    state_abb.append(state_code[i].find('td').text.strip())
# get first 80 cities and get their state_code
url_city_state = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
rq_2 = requests.get(url_city_state)
soup_2 = BeautifulSoup(rq_2.content, 'lxml')
city_state = soup_2.findAll('table')[4].findAll('tr')
sc = []
Cities = []
States = []
for i in range(1,95):
    city = city_state[i].find('a')
    Cities.append(city.text)
    all_att = city_state[i].findAll('td')
    for j in all_att:
        try:        
            if j['align'] == "left":
                if j.text.strip() not in Cities:
                    sc.append(j.text.strip())
        except:
            continue
for i in range(len(sc)):
    if '[' not in sc[i]:
        States.append(sc[i])
States_code = []
for i in States:#state_abb
    try:
        p = state.index(i)
        States_code.append(state_abb[p])
    except: 
        States_code.append(i)
for i in States_code:
    if len(i)>2:
        ind = States_code.index(i)
        States_code.pop(ind) 
        Cities.pop(ind) 
print(len(States_code))
print(len(Cities))


# In[8]:



def get_info_lists(response):
    address, postal_code, beds, baths, price, city, state, sqft,lat, lon = [], [], [], [], [], [], [], [], [] ,[]
    for i in response.json()['listings']:
        try:
            address.append(i['address'])
            postal_code.append(i['address_new']['postal_code'])
            beds.append(i['beds'])
            baths.append(i['baths'])
            price.append(i['price'])
            city.append(i['address_new']['city'])
            state.append(i['address_new']['state'])
            sqft.append(i['sqft'])
            lat.append(i['address_new']['lat'])
            lon.append(i['address_new']['lon'])
        except:
            baths.append(0)
            price.append(i['price'])
            city.append(i['address_new']['city'])
            state.append(i['address_new']['state'])
            sqft.append(i['sqft'])
            lat.append(0)
            lon.append(i['address_new']['lon'])
    return [address, postal_code, beds, baths, price, city,  state, sqft, lat, lon]

def get_into_dataframe(whole_info):
    # Convert all lists into dataframes    
    Realtor_info = {'address': [], 'postal_code': [], 'beds': [], 'baths': [], 'price': [], 'city': [],'state':[], 'sqft': [], 'lat': [], 'lon': []}
    for i in range(len(whole_info[0])):
        Realtor_info['address'].append(whole_info[0][i])
        Realtor_info['postal_code'].append(whole_info[1][i])
        Realtor_info['beds'].append(whole_info[2][i])
        Realtor_info['baths'].append(whole_info[3][i])
        Realtor_info['price'].append(whole_info[4][i])
        Realtor_info['city'].append(whole_info[5][i])
        Realtor_info['state'].append(whole_info[6][i])
        Realtor_info['sqft'].append(whole_info[7][i])
        Realtor_info['lat'].append(whole_info[8][i])
        Realtor_info['lon'].append(whole_info[9][i])
    Realtor_info_df = pd.DataFrame(Realtor_info)
    return Realtor_info_df


# In[19]:


url = "https://realtor.p.rapidapi.com/properties/list-for-sale"
whole_city = [[], [], [], [], [], [],[], [], [], []]
for i in range(82,93):
    print(i)
    querystring = {"city":f"{Cities[i]}","offset":"0","limit":"200","state_code":f"{States_code[i]}","sort":"relevance"}

    headers = {
                'x-rapidapi-key': "16faa7003bmshcd0406bc5eb2113p10829djsn452653c46812",
                'x-rapidapi-host': "realtor.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    every_city = get_info_lists(response)
    print(f'{len(every_city)},{len(whole_city)}')
    whole_city = np.concatenate((whole_city,every_city),axis=1)
Realtor_info_df = get_into_dataframe(whole_city)
print(Realtor_info_df)


# In[17]:


Realtor_info_df = get_into_dataframe(whole_city)
print(Realtor_info_df)


# In[ ]:


Realtor_info_df.to_csv("data/Realtor_info2.csv", index=False, sep=',')


# In[10]:


querystring = {"city":f"{Cities[67]}","offset":"0","limit":"5","state_code":f"{States_code[67]}","sort":"relevance"}

headers = {
        'x-rapidapi-key': "23a9ee8bc3msh2de6478f50fbeffp1a0df0jsn545042acdad5",
        'x-rapidapi-host': "realtor.p.rapidapi.com"
        }

response = requests.request("GET", url, headers=headers, params=querystring)
pprint(response.json())
#print("----"*40)
every_city = get_info_lists(response)


# In[ ]:




