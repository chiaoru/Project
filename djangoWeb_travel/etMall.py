#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 18:55:34 2023

@author: kate
"""

import requests
from datetime import datetime
import json
import re
import time
import db

url = 'https://www.etmall.com.tw/Search/Get'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    
    }

param = {
    'keyword': '瑞士',
    'PageSize': '48',
    'PageIndex': '1'

    }

today = datetime.today()
today = today.strftime('%Y-%m-%d')
product = input('請輸入欲搜尋商品：')
for i in range(0,6):
    param['PageIndex'] = i
    param['keyword'] = product
    data = requests.get(url, headers=header, params=param).text
    
    travel = json.loads(data)
    
    trip = travel['SearchProductResult']['products']
    
    for row in trip:
        title = row['title']
        title = title.replace('–', '')
        
        img = 'https:' + row['imageUrl']
        link = 'https://www.etmall.com.tw/' + row['pageLink']
    
        #describe = row['salesSubTitle']
        price = int(row['finalPrice'])
        
        describe = row['salesSubTitle']
        """
        if row['salesSubTitle'] == None:
            describe = '詳情請入內'
        #elif re.findall('([A-Z0-9/]+)',row['salesSubTitle']) != None:
        #    depDates = re.findall('([A-Z0-9/]+)',row['salesSubTitle']) # 旅行團有出發日期時才有
        #    for day in depDates:
        #        print(day, end=' ')
        else:
            describe = row['salesSubTitle']
        """
            
        print(title)
        print(describe)
        print(price)
        print(img)
        print(link)
        print()
        
        print(type(price))

        sql = "select * from Products where name='{}'".format(title)  
        cursor = db.connect.cursor() #建立資料庫物件集
        cursor.execute(sql)
        #db.cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            sql = "insert into product(platform, name, price, describe, img, link, createDate) values('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format('ETMall',title,price,describe,img,link,today)
            cursor.execute(sql)
            db.connect.commit()
            
        else:
            sql = "update product set price='{}' where name='{}'".format(price, title)
            cursor.execute(sql)
            db.connect.commit()
        
    time.sleep(1)
