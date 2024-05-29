#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 03:25:10 2023

@author: kate
"""

from django import forms
from .models import Photo

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', )
        widgets={'image':forms.FileInput(
            attrs={'class':'form-control-file'})}