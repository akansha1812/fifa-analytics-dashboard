#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:11:14 2021

@author: nikhil
"""

from flask import Flask, render_template,request, jsonify
import pandas as pd
app = Flask(__name__)


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


@app.route("/wc_filter/", methods=['GET', 'POST'])
def wc_filter():
    if request.method=='POST':
        filters = request.json
        print("Content :",filters)
        df_wc = df_clean[(df_clean.Age >= filters['age_start']) & (df_clean.Age <= filters['age_end'])]
        df_wc = df_wc[['Name','Overall','ID']]
        print("length",len(df_wc))
        s = min(len(df_wc[(df_wc['Overall'] <= 80)]),10)
        x = df_wc[(df_wc['Overall'] <= 80)].sample(n=s)
        x['Overall'] = 7
        s = min(len(df_wc[(df_wc['Overall'] < 87) & (df_wc['Overall'] > 80)]),40)
        x1 = df_wc[(df_wc['Overall'] < 87) & (df_wc['Overall'] > 80)].sample(n=s)
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