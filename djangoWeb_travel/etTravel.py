#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:18:01 2023

@author: kate
"""
# 東森旅遊
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time
import db

url = 'https://www.etholiday.com/EW/GO/GroupList.asp'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    
    }

param = {
    'displayType': 'G',
    'orderCd': '1',
    'pageALL': '1',
    'pageGO': '1',
    'pagePGO': '1',
    'waitData': 'false',
    'waitPage': 'false',
    'regmCd': '0027',
    'beginDt': '2023/11/29',
    'endDt': '2024/11/29',
    'allowJoin': '1',
    'allowWait': '1'

    }

areas = {
    '日本':'0019',
    '韓國':'0020',
    '越南/緬甸':'0021',
    '泰國':'0022',
    '菲律賓':'0023',
    '印尼(峇里島)':'0024',
    '馬來西亞/新加坡':'0026',
    '歐洲':'0027',
    '紐澳':'0029',
    '島嶼自由行':'0042',
    '中東':'0061'
        }


print(areas.keys())
area = input('請輸入想去的區域名稱：')
code = areas.get(area)

for i in range(1, 3):
    param['regmCd'] = code
    param['pageALL'] = i
    data = requests.post(url, headers=header, data=param).text
    
    soup = BeautifulSoup(data,'html.parser')
    
    tours = soup.find('div', class_='products')
    
    alltours = tours.find_all('div', class_='product product_item item')
    
    today = datetime.today()
    now = today.strftime('%Y-%m-%d')
    
    for row in alltours:
        platform = '東森旅遊'
        title = row.find('div', class_='product_name').text.replace('\n','')
        title = title.replace(' ', '')
        
        priceInfo = row.find('div', class_='product_price')
        priceInfo = priceInfo.find('span').text
        price = re.findall('([A-Z0-9]+)', priceInfo)
        price = price[0] + price[1]
        
        depDate = row.find('div', class_='product_date normal').text
        img = row.find('img').get('src')
        img = 'https://www.etholiday.com/' + img
        
        link = row.find('a').get('href')
        link = 'https://www.etholiday.com' + link
        #print(platform)
        #print(area)
        print(title)
        #print(price)
        #print(depDate)
        #print(img)
        #print(link)
        #print(now)
        
        sql = "select * from tours where platform='{}' and title='{}' and depDate='{}'".format(platform, title, depDate)
        db.cursor.execute(sql)
        result = db.cursor.fetchone()
        if result == None:
            sql = "insert into tours(platform, area, title, price, depDate, img, link, createDate) values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(platform, area, title, price, depDate, img, link, now)
            db.cursor.execute(sql)
            db.connect.commit()
            
        elif result != None:
            sql = "update tours set price='{}' where title='{}'".format(price, title)
            db.cursor.execute(sql)
            db.connect.commit()
        
        time.sleep(1)
            
#db.connect.close()



