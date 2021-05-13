#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 22:17:18 2021

@author: nikhil
"""
import pandas as pd

f = open("static/position-map.txt","r")
position_map = {}
for line in f:
    pos = line.split("\t")[0]
    # print(pos)
    nos = line.split("\t")[1].replace("\n", "").replace(" ", "").split(",")
    # print(nos)
    for n in nos:
        # print(n)
        position_map[int(n)]=pos
# print(position_map)
df_clean = pd.read_csv("static/fifa_processed_final.csv")
df_clean = df_clean.loc[df_clean['ID'].astype(str)== str(20801)]
print(int(df_clean['RW'].values[0].split("+")[0]))
print(df_clean)