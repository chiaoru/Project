#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:42:22 2023

@author: kate
"""

# Swiss Info 瑞士新聞網
import requests
from bs4 import BeautifulSoup
import time
import db

url = 'https://www.swissinfo.ch/eng/search/travel'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    }

param = {

    #'query' :'旅遊',
    'page':'1',
    
    }

for i  in range(0,2):
    param['page'] = i
    
    data = requests.get(url, headers=header, params=param).text

    soup = BeautifulSoup(data, 'html.parser')

    news = soup.find(id='main-content')

    allnews = news.find_all('article')
    
    for row in allnews:
        title = row.find('h3').text.strip()
        link = row.find('a').get('href')
        try:
            img = row.find('img').get('src')
        except AttributeError:
            img = ''
        
        if not ('http' in img):
            img = 'https://www.swissinfo.ch' + img
            
        
        info = row.find('p', class_='teaser-wide-card__excerpt')
        times = row.find('time', class_='teaser-wide-card__published/datetime').text.strip()
        describe = info.find('span', class_='teaser-wide-card__excerpt/truncator').text.strip()
        
        platform = 'SwissInfo'
        
        print(title)
        #print(times)
        #print(describe)
        #print(img)
        #print(link)
        #print()
        
        sql = "select * from news where platform='{}' and title='{}'".format(platform, title)
        db.cursor.execute(sql)
            
        result = db.cursor.fetchone()
        if result == None:
            if len(link) > 255:
                sql = "insert into news(platform, title, content, img, link, createDate) values('{}', '{}', '{}', '{}', '{}', '{}')".format(platform, title, describe, img, '', times)
                
            else:
                sql = "insert into news(platform, title, content, img, link, createDate) values('{}', '{}', '{}', '{}', '{}', '{}')".format(platform, title, describe, img, link, times)
                
            db.cursor.execute(sql)
            db.connect.commit()
        
    time.sleep(1)
    
    
    
db.connect.close()
    
    
    
    
    
    
    
    