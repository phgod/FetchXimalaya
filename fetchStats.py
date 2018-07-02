#!/usr/bin/python3

######################################################################
# Simple web scraper to fetch read count information from Ximalaya
# Requires: Python 3
# How to run: ./fetchStats.py (make sure it has run persmission)
# 20180630 - Haoran Zhang
######################################################################

import urllib.request as req # for python 3

# Make the request. Note that nothing will be returned if user agent is not specified.
q = req.Request("http://www.ximalaya.com/shangye/16141838/")
q.add_header('User-Agent', 'Mozilla/5.0')
page = req.urlopen(q).read()

# Fetch the contents
from bs4 import BeautifulSoup
soup = BeautifulSoup(page, "lxml")

# Get the audio information
import re
author=[]
title=[]
category=[]
all_audios = soup.find_all("div", class_='e-2304105070 text')
for a in all_audios:
    info = re.search(r'\uff5c(.*)\uff1a(.*)\u3010(.*)\u300b(.*)', a.find("a").get("title"))
    author.append(info.group(1)[:-2]) # Drop the author title
    title.append(info.group(2))
    category.append(info.group(4)[:2]) # Only take the first two words

# Get the count
count=[]
all_counts = soup.find_all("span", class_='e-2304105070 count')
for c in all_counts:
    count.append(int(c.find(text=True)))

# Timestamp
import datetime
dt = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

# Put all the data into data frame
import pandas as pd
stats = pd.DataFrame({'author': author,'title':title, 'category':category, 'count':count, 'timestamp':dt}, 
    columns=['timestamp', 'author', 'title', 'category', 'count'])

print("The following dataframe will be written to file:")
print(stats)

# Write data to csv
import os.path
stats.to_csv('count.csv', encoding="utf-8", mode='a', index=False, header=False if os.path.isfile('count.csv') else True)

