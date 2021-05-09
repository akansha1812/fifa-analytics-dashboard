#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:28:56 2021

@author: nikhil
"""

#Preprocessing raw data
import pandas as pd
df = pd.read_csv("static/fifa_data_manual.csv")
df['Release Clause'] = df['Release Clause'].fillna(0)
df['Value'] = df['Value'].str.replace('€','')
df.Value = (df.Value.replace(r'[KMB]+$', '', regex=True).astype(float) * df.Value.str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df['Wage'] = df['Wage'].str.replace('€','')
df.Wage = (df.Wage.replace(r'[KMB]+$', '', regex=True).astype(float) * df.Wage.str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
from dateutil.parser import parse
import datetime
def clean_date(text):
  datetimestr = parse(text)
  text = datetime.strptime(datetimestr, '%Y%m%d')
  return text
df['Contract Valid Until'] = df['Contract Valid Until'].replace(r'\d{1,2}-\w{3}-', '20', regex=True)
df['Release Clause'] = df['Release Clause'].str.replace('€','')
df['Release Clause'] = (df['Release Clause'].replace(r'[KMB]+$', '', regex=True).astype(float) * df['Release Clause'].str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df.to_csv('static/fifa_processed_final.csv')


#Processing data for Choropleth Map
Nation = pd.DataFrame(df.Nationality.value_counts().reset_index().values, columns=["nation", "frequency"])
NationIndex = Nation.sort_index(axis = 0, ascending=True)
NationIndex["id"]=""
import json
f = open('static/world_countries.json',)
data = json.load(f)
for i, row in NationIndex.iterrows():
    nation = row['nation']
    for j in range(177):
        country = data['features'][j]['properties']['name']
        if country=="United States":
                print(2)
        if country==nation:
            if country=="United States":
                print(3)
            id = data['features'][j]['id']
            NationIndex.at[i,'id']=id

NationIndex['id'] = NationIndex['id'].fillna(0)
NationIndex.to_csv('nationality_counts.csv')


#Processing data for Line Chart
age_counts = pd.DataFrame(df.Age.value_counts().reset_index().values, columns=["age", "frequency"])
age_counts = age_counts.sort_index(axis = 0, ascending=True)
age_counts = age_counts.sort_values(by=['age'])
age_counts.to_csv('age_counts.csv')