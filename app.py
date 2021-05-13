#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:11:14 2021

@author: nikhil
"""
from os import path
if not path.exists("static/fifa_processed_final.csv"):
    exec(open("pre_processing.py").read())


from flask import Flask, render_template,request, jsonify
import random
import pandas as pd
app = Flask(__name__)

df_clean = pd.read_csv("static/fifa_processed_final.csv")
df_pos_map = pd.read_csv("static/test_pitch.csv")



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
    result = list(df_sc_T.T.to_dict().values())
    return jsonify(result)


@app.route("/player_card/<prop>")
def player_card(prop):
    df_sc = df_clean.copy()
    df_sc = df_sc.loc[df_sc['ID'].astype(str)== str(prop)]
    df_sc = df_sc[['Name','Age','Nationality','Club','Overall']]
    result = list(df_sc.T.to_dict().values())
    print(result)
    return jsonify(result)



@app.route("/pcp/<prop>")
def pcp(prop):
    prop = str(prop)
    df_pcp = df_clean.copy()
    if prop!='world':
        df_pcp = df_pcp.loc[df_pcp['Country'].astype(str) == str(prop)]
    df_pcp = df_pcp[['Club','Age','Value','Wage','Overall','Release Clause']]
    attr_cols = ['Age','Value','Wage','Overall','Release Clause']
    df_pcp_agg = df_pcp.groupby("Club").mean()
    df_pcp_agg['Wage'] = df_pcp_agg['Wage'].astype(str).astype(float)
    df_pcp_agg['Club'] = df_pcp_agg.index
    s = min(len(df_pcp_agg),22)
    df_pcp_agg = df_pcp_agg.sample(n = s)
    result = list(df_pcp_agg.T.to_dict().values())
    return jsonify(result)

@app.route("/club_logos/<prop>")
def club_logos(prop):
    prop = str(prop)
    df_cl = df_clean.copy()
    if prop!='world':
        df_cl = df_cl.loc[df_cl['Country'].astype(str) == str(prop)]
    df_cl = df_cl[['Club']]
    df_cl.drop_duplicates(subset ="Club",keep = False, inplace = True)
    s = min(len(df_cl),15)
    df_cl = df_cl.sample(n = s)
    result = list(df_cl.T.to_dict().values())
    return jsonify(result)


@app.route("/pitch_plot/<prop>")
def pitch_plot(prop):
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
    df_sc = df_clean.copy()
    df_sc = df_sc.loc[df_sc['ID'].astype(str)== str(prop)]
    pos_list = ['LS','ST','RS','LW','LF','CF','RF','RW','LAM','CAM','RAM','LM','LCM','CM','RCM','RM','LWB','LDM','CDM','RDM','RWB','LB','LCB','CB','RCB','RB']
    df_sc_pos = df_sc[pos_list]
    df_sc_pos = df_sc_pos.apply(lambda x: (x-x.min())/(x.max()-x.min()), axis=1)
    for i, row in df_pos_map.iterrows():
        x = position_map[i+1]
        if df_sc['Position'].values[0]=='GK':
            gk_cols = ['GKDiving','GKHandling','GKKicking','GKPositioning','GKReflexes']
            y = df_sc[gk_cols].astype(str).astype(float).mean(axis=1)
            if x=='GK':
                df_pos_map.at[i,'ratio_origin'] = y/10
            else:
                df_pos_map.at[i,'ratio_origin'] = 0.2
        else:
            if x=='GK':
                df_pos_map.at[i,'ratio_origin'] = 0.1
            else:
                # y = int(df_sc[x].values[0].split("+")[0])/10
                # print(y)
                # df_pos_map.at[i,'ratio_origin'] = int(df_sc[x].values[0].split("+")[0])/100
                df_pos_map.at[i,'ratio_origin'] = df_sc_pos[x].values[0]
    
    result = list(df_pos_map.T.to_dict().values())
    # print("Player heat Map : ",result)
    return jsonify(result)
    


@app.route("/wc_filter/", methods=['GET', 'POST'])
def wc_filter():
    df_wc = df_clean.copy()
    if request.method=='POST':
        filters = request.json
        if filters['country_name'] != 'world':
            df_wc = df_wc.loc[df_wc['Country'] == filters['country_name']]
        df_wc = df_wc[(df_wc.Age >= filters['age_start']) &
                         (df_wc.Age <= filters['age_end']) &
                         (df_wc.Value >= filters['value_start']) &
                         (df_wc.Value <= filters['value_end']) &
                         (df_wc.Overall >= filters['rating_start'])]
        df_wc = df_wc[['Name','Overall','ID']]
        s = min(len(df_wc[(df_wc['Overall'] <= 80)]),20)
        x = df_wc[(df_wc['Overall'] <= 80)].sample(n=s)
        x['Overall'] = 5
        s = min(len(df_wc[(df_wc['Overall'] <= 87) & (df_wc['Overall'] > 80)]),45)
        x1 = df_wc[(df_wc['Overall'] <= 87) & (df_wc['Overall'] > 80)].sample(n=s)
        x1['Overall'] = 7
        x = x.append(x1)
        x1 = df_wc[(df_wc['Overall'] <= 90) & (df_wc['Overall'] > 87)]
        x1['Overall'] =10
        x = x.append(x1)
        x1 = df_wc[(df_wc['Overall'] <= 92) & (df_wc['Overall'] > 90)]
        x1['Overall'] = 20
        x = x.append(x1)
        x1 = df_wc[(df_wc['Overall'] > 92)]
        x1['Overall'] = 30
        x = x.append(x1)
        x = x.sample(frac=1)
        
        l = []
        for i in range(256):
            l.append(i)
        random_num = random.choice(l)
        x['c'] = (x.index+100)%256 +1
        result = list(x.T.to_dict().values())

    return jsonify(result)



@app.route("/linePlot/<prop>/<prop2>")
def linePlot(prop,prop2):
    country_name = str(prop)
    column_name = str(prop2)
    df = df_clean.copy()
    if country_name != 'world':
        df = df.loc[df['Country'].astype(str) == str(country_name)]
    age_counts = pd.DataFrame(df[column_name].value_counts().reset_index().values, columns=[column_name, "frequency"])
    age_counts = age_counts.sort_index(axis=0, ascending=True)
    age_counts = age_counts.sort_values(by=[column_name])
    result = list(age_counts.T.to_dict().values())
    return jsonify(result)


if __name__ == '__main__':
    app.run()