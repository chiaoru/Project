#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 17:55:20 2023

@author: kate
"""

# 東南旅遊
import requests
from bs4 import BeautifulSoup
import re
import time
import db
from datetime import datetime


url = ' https://tour.settour.com.tw/search'

param = {
    'arrDate': '20240831',
'depDate': '20231121',
'destinationCode': 'CH_3',
'isChaFly': 'false',
'isGoEarly': 'false',
'isLateReturn': 'false',
'isMiniTour': 'true',
'isMkt': 'false',
'isNoPay': 'false',
'isNoShopping': 'false',
'isOffer': 'false',
'isOnlyMiniTour': 'false',
'isOrderFlag': 'true',
'isPakFly': 'false',
'keyWords':'',
'maxValue': '-1',
'minValue': '-1',
'pageNum': '1',
'portType': 'B2C',
'sortType': 'BA'

    }


header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'
    
    }

areas = {
    '東北亞':'1A_ALL',
    '日本':'1A1_2',
    '韓國':'1A2_2',
    '東南亞':'1Ｃ_ALL',
    '泰國':'1C1_2',
    '馬來西亞/新加坡':'1C2_2',
    '印尼':'1C3_2',
    '菲律賓':'1C4_2',
    '中南半島':'1C5_2',
    '港澳大陸全區':'1B_ALL',
    '華北':'1B1_2',
    '東北':'1B2_2',
    '華東':'1B3_2',
    '華中':'1B4_2',
    '西南':'1B5_2',
    '西北':'1B7_2',
    '華南':'1B6_2',
    '港澳大陸':'1B8_2',
    '蒙古':'1B9_2',
    '美洲':'1D_ALL',
    '美國':'1D1_2',
    '加拿大':'1D2_2',
    '歐洲':'1E_ALL',
    '中西歐':'1E1_2',
    '東歐':'1E2_2',
    '南歐':'1E3_2',
    '北歐':'1E4_2',
    '紐澳':'1F_ALL',
    '澳洲':'1F1_2',
    '紐西蘭':'1F2_2',
    '太平洋島嶼':'1F3_2',
    '南亞/中亞非':'1G_ALL',
    '南亞':'1G1_2',
    '中東':'1G2_2',
    '非洲':'1G1_2'
        }

print(areas.keys())
area = input('請輸入想去的區域名稱：')

code = areas.get(area)

param['destinationCode'] = code

today = datetime.today()
now = today.strftime('%Y-%m-%d')

if code == None:
    print("找不到此區域！")
else:
    p = input('請輸入想去的城市/國家名稱：')
    param['keyWords'] = p
    
    for i in range(1,4):
        param['pageNum'] = i

        data = requests.get(url, headers=header, params=param).text
        
        soup = BeautifulSoup(data,'html.parser')
        
        tours = soup.find('div', class_='product')
        
        try:
            
            tour = tours.find_all('article', class_='product-item tour')
            
        except AttributeError:
            pass
        
        for row in tour:
            title = row.find('h4').text
            img  = row.find('img').get('src')
            price = row.find('div', class_='ori-price-offer').text
            price = re.findall('([A-Z0-9]+)', price)
            price = price[0] + price[1]
            
            depDate = row.find('div', class_='product-item-right-text').text.split('，')
            depDate = depDate[0]
            
            groupNumber = row.find('div', class_='product-info-bottom hidden-md hidden-sm hidden-xs').text
            groupNumber = re.findall('([A-Z0-9]+)', groupNumber)[0]
            
            link = img.split('%2F')
            link = 'https://tour.settour.com.tw/product/' + link[4] + link[5] + link[6] + link[7] + '/' + groupNumber
            
            print(area)
            print(title)
            print(price)
            print(depDate)
            print(img)
            print(link)
            
            platform = '東南旅遊'
            
            
            
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

    
    