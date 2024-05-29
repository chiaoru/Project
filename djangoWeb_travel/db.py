#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 01:19:53 2023

@author: kate
"""

import pymysql

# 可用 import db (寫在另一個專門的檔案中) 代替
dbsetting = {
    "host":"127.0.0.1",
    "port":3306,
    "user":"root",
    "password":"",
    "db":"tourProject",
    "charset":"utf8"
    }

connect = pymysql.connect(**dbsetting)

# 函數：無參數、預設值參數，* -> 串列 ** -> 字典

# 跟mysql 溝通語法時，需要產生一個資料庫物件
cursor = connect.cursor() # cursor = db.connect.cursor()