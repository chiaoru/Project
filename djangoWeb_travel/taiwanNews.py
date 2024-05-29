#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 15:44:45 2022

@author: kate
"""

import db
from bs4 import BeautifulSoup
import requests

import datetime



# 三立新聞
setn = "https://www.setn.com/ViewAll.aspx?PageGroupID=0&utm_source=setn.com&utm_medium=menu&utm_campaign=hotnews"

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    }

data = requests.get(setn, headers=header).text

soup = BeautifulSoup(data,'html.parser')

news = soup.find_all('div', class_='col-sm-12 newsItems')


for row in news:
    h3 = row.find('h3') # 標題、連結
    link = h3.find('a').get('href')
    if not ('http' in link):
        link = 'https://www.setn.com' + link
    title = h3.text
    
#    print(item)
    print(title)
#    print(link)
    print()

    platform = '三立新聞'
    img = 'https://play-lh.googleusercontent.com/0PbIPJMouqva1mrodsDHHTb0tGjEi7hxWVGAGV0XjTbRWd34NWJlmzVhtLzJZWzS1bA'
    
    sql = "select * from news where platform='{}' and title='{}'".format(platform, title)
    db.cursor.execute(sql)
        
    result = db.cursor.fetchone()
    if result == None:
        today = datetime.datetime.today()
        now = today.strftime('%Y-%m-%d')
        now = str(now)
        sql = "insert into news(platform, title, content, img, link, createDate) values('{}', '{}', '{}', '{}', '{}', '{}')".format(platform, title, '', img, link, now)
        db.cursor.execute(sql)
        db.connect.commit()
       

# TVBS NEWS

tvbs = 'https://news.tvbs.com.tw/realtime'

data = requests.get(tvbs,headers=header).text

soup = BeautifulSoup(data,'html.parser')

news = soup.find('div',class_='news_list')

news = news.find('div',class_='list') # 因為被其他埋入的li影響，所以要抓更細

allNews = news.find_all('li')

for row in allNews:
    a = row.find('a') # 避免沒有a找不到
    if  not (a == None):
        
        title = row.find('h2').text
        img = row.find('img').get('data-original')
        link = row.find('a').get('href')
        if not ('http' in link):
            link = 'https://news.tvbs.com.tw' + link
        platform = 'TVBS'
        
#        print(item)
        print(title)
#        print(img)
#        print(link)
        print()
        
        sql = "select * from news where platform='{}' and title='{}'".format(platform, title)
        db.cursor.execute(sql)
            
        result = db.cursor.fetchone()
        if result == None:
            today = datetime.datetime.today()
            now = today.strftime('%Y-%m-%d')
            now = str(now)
            sql = "insert into news(platform, title, content, img, link, createDate) values('{}', '{}', '{}', '{}', '{}', '{}')".format(platform, title, '', img, link, now)
            db.cursor.execute(sql)
            db.connect.commit()
        
# 東森新聞

ebc = 'https://news.ebc.net.tw/realtime'

data = requests.get(ebc,headers=header).text

soup = BeautifulSoup(data,'html.parser')

news = soup.find_all('div',class_='style1 white-box')

for row in news:
    title = row.find('a').get('title')
    img = row.find('img').get('src')
    link = row.find('a').get('href')
    if not ('http' in link):
        link = 'https://news.ebc.net.tw' + link
    platform = '東森新聞'
    print(title)

    sql = "select * from news where platform='{}' and title='{}'".format(platform, title)
    db.cursor.execute(sql)
        
    result = db.cursor.fetchone()
    if result == None:
        today = datetime.datetime.today()
        now = today.strftime('%Y-%m-%d')
        
        sql = "insert into news(platform, title, content, img, link, createDate) values('{}', '{}', '{}', '{}', '{}', '{}')".format(platform, title, '', img, link, now)
        db.cursor.execute(sql)
        db.connect.commit()

"""
# 華視新聞

cts = 'https://news.cts.com.tw/real/index.html'

data = requests.get(cts,headers=header)
data.encoding = 'utf-8'
data = data.text

soup = BeautifulSoup(data,'html.parser')

news = soup.find(id='newslist-top')
allNews = news.find_all('a')

for row in allNews:
    title = row.get('title')
    if not(title == None):
        img = row.find('img').get('data-src')
        link = row.get('href')
        
        sql = "select * from news where station='華視新聞' and title='{}'".format(title)
        cursor = db.connect.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0: # 表示沒有資料
            today = datetime.datetime.today()
            now = today.strftime('%Y-%m-%d')
            sql = "insert into news(station,title,category,photo_url,news_url,create_date) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,['華視新聞',title,'',img,link,now])
            db.connect.commit()
        

"""


db.connect.close()


