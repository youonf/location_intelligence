#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import json
from random import randint
from time import sleep
import requests
from tqdm import tqdm
import numpy as np


# ### Clan the district, cuisine, dish columns

# In[3]:


df = pd.read_csv('restaurant_clean.csv', index_col=0)


# In[ ]:


with open('all_restaurant.json', 'w') as f:
    json.dump({}, f)


# In[15]:


re_dict={}


# In[18]:


def ogcioparser_dict(address):
    data = {"q":address, "n":1} #n means only send 1 
    headers ={"Accept": "application/json"}
    api_url = "https://www.als.ogcio.gov.hk/lookup"
    res = requests.post(api_url, data=data, headers=headers, timeout=(5, 14))
    add = json.loads(res.text)
    add_dict = {}
    add_dict['Latitude'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Latitude']    
    add_dict['Longitude'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Longitude']
    add_dict['Easting'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Easting']
    add_dict['Northing'] = add['SuggestedAddress'][0]['Address']['PremisesAddress']['GeospatialInformation'][0]['Northing']
    return add_dict

# In[28]:


addresses = df['address']


# In[31]:


sleep_counter = 0


# In[32]:


all_dict = {}
working_dict = {}
for i, a in enumerate(tqdm(addresses)):
    parse = ogcioparser_dict(a)
    all_dict[i] = parse
    working_dict[i] = parse
    sleep_counter +=1
    if sleep_counter % 500 == 0:
        sleep(randint(5,10))

        with open('all_restaurant.json') as f:
            file = json.load(f)

        file.update(working_dict)

        with open('all_restaurant.json', 'w') as f:
            json.dump(file, f)
            
        working_dict = {}


# In[26]:


df_parse = pd.DataFrame.from_dict(all_dict, orient='index')


# In[ ]:


df_parse.to_csv('parse.csv')

