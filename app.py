#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:11:14 2021

@author: nikhil
"""

from flask import Flask, render_template,request, jsonify
import pandas as pd
from sklearn.decomposition import PCA
import preprocess
import json
import math
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
app = Flask(__name__)


def get_top_4_loading(n,pca_components):
    ss_list = []
    for j in range(len(pca_components)):
        sum = 0.0
        for i in range(n):
            sum = sum + (pca_components[i][j])**2
        ss_list.append(math.sqrt(sum))
    
    ss_list = np.asarray(ss_list, dtype=np.float64)
    indices = ss_list.argsort()[-4:][::-1]
    return ss_list, indices

def getbiplotdata(df_lg, pca_components):
    df_lg_np = df_lg.to_numpy()
    x_updated = []
    y_updated = []
    for act_val in df_lg_np:
        sum = 0
        i=0
        for pc_val in pca_components[0]:
            sum = sum + act_val[i]*pc_val
            i = i+1
        x_updated.append(sum)
        
    for act_val in df_lg_np:
        sum = 0
        i=0
        for pc_val in pca_components[1]:
            sum = sum + act_val[i]*pc_val
            i = i+1
        y_updated.append(sum)
    pca_biplot_points = []
    for i in range(len(x_updated)):
        pca_biplot_points.append({'PC1':x_updated[i],'PC2':y_updated[i]})
    coordinate_list = []
    for x in range(2):
        l1=[]
        for y in range(len(pca_components[x])):
            l1.append(pca_components[x][y])
        coordinate_list.append(l1)
    pca_line_data = []
    # print(coordinate_list)
    for i in range(len(coordinate_list[0])):
        pca_line_data.append({'X':coordinate_list[0][i],'Y':coordinate_list[1][i]})
    # print(pca_line_data)
    return pca_biplot_points, pca_line_data

@app.route('/lab1_home')
def lab1_home():
    return render_template('homepage.html')

# @app.route('/home')
# def home():
#     return render_template('home.html')

@app.route('/lab2a_home', methods = ['GET','POST'])
def lab2a_home():
    df_lg = preprocess.process_csv("static/asteroid_6k.csv")
    n = len(df_lg.columns)
    pca = PCA(n_components=n)
    principalComponents = pca.fit_transform(df_lg)
    eigen_val = pca.explained_variance_ratio_
    eigen_val_perc = []
    i = 1
    sum = 0
    for val in eigen_val:
        sum = sum+eigen_val[i-1]*100
        eigen_val_perc.append({'pc_no':i,'percentage':eigen_val[i-1]*100,'cum':sum})
        i = i+1
    pca_biplot_points, pca_line_data = getbiplotdata(df_lg, pca.components_)
    if request.method=='POST':
        jsdata = request.form['jsdata']
        scrollpos = request.form['scrollpos']
        # print("scrollpos",scrollpos)
        # print(jsdata)
        ss_list, top_att_indices = get_top_4_loading(int(jsdata), pca.components_)
        top_att_arr =[]
        i=1
        col_name_arr = []
        for index in top_att_indices:
            arr = []
            arr.append(i)
            i = i+1
            arr.append(df_lg.columns[index])
            col_name_arr.append(df_lg.columns[index])
            arr.append(ss_list[index])
            top_att_arr.append(arr)
        # print(json.dumps(col_name_arr))
        return render_template('lab2a_home.html',pca_biplot_points=json.dumps(pca_biplot_points),pca_line_data=json.dumps(pca_line_data),scrollpos=scrollpos,flag=1,pca=jsdata,eigen_val_perc=json.dumps(eigen_val_perc),top_att_arr=top_att_arr,col_name_arr=json.dumps(col_name_arr))
    else:
        return render_template('lab2a_home.html',pca_biplot_points=json.dumps(pca_biplot_points),pca_line_data=json.dumps(pca_line_data),flag=0,pca=0,eigen_val_perc=json.dumps(eigen_val_perc))


@app.route('/lab2b_home', methods = ['GET','POST'])
def lab2b_home():
    return render_template('lab2b_home.html')

@app.route('/test', methods = ['GET','POST'])
def test():
    return render_template('test.html')





@app.route("/spiderChart/<prop>")
def spiderChart(prop):
    df_sc = df_clean.copy()
    df_sc = df_sc.loc[df_sc['ID'].astype(str)== str(prop)]

    # print(df_sc)
    #define cols
    striking_cols = ['Finishing','Volleys','Penalties','ShotPower','LongShots','Positioning']
    dribbling_cols = ['Dribbling','Agility','Reactions','Balance','BallControl','Composure']
    passing_cols = ['Curve','Crossing','FKAccuracy','LongPassing','ShortPassing','Vision']
    defence_cols = ['HeadingAccuracy','Interceptions','Marking','StandingTackle','SlidingTackle']
    physical_cols = ['Aggression','Jumping','Stamina','Strength','SprintSpeed']
    gk_cols = ['GKDiving','GKHandling','GKKicking','GKPositioning','GKReflexes']

    df_sc['Striking'] = df_sc[striking_cols].astype(str).astype(float).mean(axis=1)
    df_sc['Dribbling Ability'] = df_sc[dribbling_cols].astype(str).astype(float).mean(axis=1)
    df_sc['Passing'] = df_sc[passing_cols].astype(str).astype(float).mean(axis=1)
    df_sc['Defending'] = df_sc[defence_cols].astype(str).astype(float).mean(axis=1)
    df_sc['Physical'] = df_sc[physical_cols].astype(str).astype(float).mean(axis=1)
    df_sc['Goalkeeping'] = df_sc[gk_cols].astype(str).astype(float).mean(axis=1)

    df_sc = df_sc[['Striking','Dribbling Ability','Passing','Defending','Physical','Goalkeeping']]
    df_sc_T = df_sc.T
    df_sc_T['axis'] = df_sc_T.index
    df_sc_T = df_sc_T.rename(columns = {df_sc_T.columns[0]: "value"})
    print(df_sc_T)
    # print(df_sc.columns)
    result = list(df_sc_T.T.to_dict().values())
    print(result)
    return jsonify(result)


@app.route("/player_card/<prop>")
def player_card(prop):
    df_sc = df_clean.copy()
    df_sc = df_sc.loc[df_sc['ID'].astype(str)== str(prop)]
    df_sc = df_sc[['Name','Age','Nationality','Club','Overall']]
    result = list(df_sc.T.to_dict().values())
    print("Player Card " , result)
    return jsonify(result)



@app.route("/pcp")
def pcp():
    df_pcp = df_clean[['Club','Age','Value','Wage','Overall','Release Clause']]
    attr_cols = ['Age','Value','Wage','Overall','Release Clause']
    df_pcp_agg = df_pcp.groupby("Club").mean()
    df_pcp_agg['Wage'] = df_pcp_agg['Wage'].astype(str).astype(float)
    df_pcp_agg['Club'] = df_pcp_agg.index
    df_pcp_agg = df_pcp_agg.sample(n = 15)
    print(df_pcp_agg)
    result = list(df_pcp_agg.T.to_dict().values())
    return jsonify(result)


df_clean = pd.read_csv("static/fifa_processed_final.csv")

@app.route("/wc")
def wc():
    df_wc = df_clean[['Name','Overall']]
    x = df_wc[(df_wc['Overall'] <= 80)].sample(n=10)
    x['Overall'] = 7
    x1 = df_wc[(df_wc['Overall'] < 87) & (df_wc['Overall'] > 80)].sample(n=40)
    x1['Overall'] = 10
    x = x.append(x1)
    x1 = df_wc[(df_wc['Overall'] < 90) & (df_wc['Overall'] > 87)]
    x1['Overall'] =15
    x = x.append(x1)
    x1 = df_wc[(df_wc['Overall'] <= 92) & (df_wc['Overall'] > 90)]
    x1['Overall'] = 25
    x = x.append(x1)
    x1 = df_wc[(df_wc['Overall'] > 92)]
    x1['Overall'] = 40
    x = x.append(x1)
    x = x.sample(frac=1)
    x['c'] = (x.index)%9 +1
    result = list(x.T.to_dict().values())
    return jsonify(result)
    
if __name__ == '__main__':
    app.run()