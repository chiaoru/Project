#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 03:01:05 2023

@author: kate
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.gallery, name='gallery'),
]