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


with open('data.json') as f:
    data = json.load(f)


# In[2]:


df = pd.DataFrame(columns =['name','review','bookmark','smile','sad','address','district','cuisine','dish'])


# In[236]:


for k in tqdm(range(len(data))):
    soup = BeautifulSoup(data[str(k)], "html.parser")
    for i in range(len(soup.find_all(class_='title-name'))):
        rest = {}
        rest['name'] = soup.find_all(class_='title-name')[i].text.strip()
        review = soup.find_all(class_="counters-container")[i].text.strip()
        rest['review'] = int(*re.findall('\d+', review))
        rest['bookmark'] = soup.find_all(class_="text bookmarkedUserCount js-bookmark-count")[i]['data-count']
        rest['smile'] = soup.find_all(class_="emoticon-container smile-face pois-restaurant-list-cell-content-right-info-rating-happy")[i].text.strip()
        rest['sad'] = soup.find_all(class_="emoticon-container sad-face pois-restaurant-list-cell-content-right-info-rating-sad")[i].text.strip()
        rest['address'] = soup.find_all(class_='icon-info-wrapper')[i].find('span').find(text=True).strip()
        rest['district'] = soup.find_all(class_='icon-info-wrapper')[i].find('a').text
        rest['cuisine'] = soup.find_all(class_="icon-info icon-info-food-name")[i].find_all('a')[0].text
        rest['dish'] = soup.find_all(class_="icon-info icon-info-food-name")[i].find_all('a')[1].text
        df = df.append(rest, ignore_index=True)


# In[ ]:


df.to_csv('restaurant.csv')


# In[ ]:




