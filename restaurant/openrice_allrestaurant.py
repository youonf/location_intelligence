#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
from random import randint
from time import sleep
import requests
from tqdm import tqdm
import numpy as np


# ### Clan the district, cuisine, dish columns


df = pd.read_csv('restaurant_clean.csv', index_col=0)


# In[18]:


def ogcioparser_dict(address):
    data = {"q":address, "n":1} #n means only send 1 
    headers ={"Accept": "application/json"}
    api_url = "https://www.als.ogcio.gov.hk/lookup"
    res = requests.post(api_url, data=data, headers=headers, timeout=(5, 14))
    add = json.loads(res.text)
    add_dict = {}
    add_dict['Northing'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Northing']
    add_dict['Easting'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Easting']
    add_dict['Longitude'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Longitude']
    add_dict['Latitude'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Latitude']
    return add_dict


# In[28]:


addresses = df['address']


# In[29]:


all_dict = {}


# In[31]:


sleep_counter = 0


# In[32]:

for i, a in enumerate(tqdm(addresses)):
    all_dict[i] = ogcioparser_dict(a)
    sleep_counter +=1
    if sleep_counter % 500 == 0:
        sleep(randint(5,10))


# In[ ]:

df_parse = pd.DataFrame.from_dict(all_dict, orient='index')

df_parse.to_csv('parse.csv')