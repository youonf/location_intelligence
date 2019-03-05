#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm
import json


# In[3]:


with open('data.json', 'w') as f:
    json.dump({}, f)


# In[ ]:


data={}
for j in tqdm(range(0,1843)):
    url = "https://www.openrice.com/en/hongkong/restaurants?sortBy=BookmarkedDesc&page="
    page = j+1
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    response = requests.get(url+"?page="+str(j), headers=headers)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    
    content = soup.find(class_='sr1-listing-content-cells pois-restaurant-list js-poi-list-content-cell-container')
    
    data[j] = content.prettify()
    
    if j % 10 == 0:
        with open('data.json') as f:
            file = json.load(f)

        file.update(data)

        with open('data.json', 'w') as f:
            json.dump(file, f)
            
        data = {}


# In[ ]:




