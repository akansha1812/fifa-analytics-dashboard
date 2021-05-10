#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 01:30:48 2021

@author: nikhil
"""

import openpyxl
from openpyxl_image_loader import SheetImageLoader
#loading the Excel File and the sheet
pxl_doc = openpyxl.load_workbook('club_images.xlsx')
sheet = pxl_doc['England']
#calling the image_loader
image_loader = SheetImageLoader(sheet)
#get the image (put the cell you need instead of 'A1')
image = image_loader.get('A5')
#showing the image
#image.show()
#saving the image
image.save('static/club_logo/'+sheet["B5"].value+'.png')