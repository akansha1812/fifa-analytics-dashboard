#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 04:46:02 2021

@author: nikhil
"""


import pandas as pd
from sklearn.decomposition import PCA

def process_csv(csv_file):
    df_lg = pd.read_csv(csv_file)
    df_lg['mag_slope'] = df_lg['mag_slope'].fillna(0)
    df_lg['bv_mag_difference'] = df_lg['bv_mag_difference'].fillna(0)
    df_lg['ub_mag_difference'] = df_lg['ub_mag_difference'].fillna(0)
    df_lg['albedo'] = df_lg['albedo'].fillna(0)
    df_lg['rotation_period'] = df_lg['rotation_period'].fillna(0)
    
    normalize_columns = ['sm_axis','eccentricity','mag_slope','incline','longitude','argument_of_perihelion','perihelion_distance','aphelion_distance','orbital_period','data_arc','no_obs_used','absolute_magnitude_parameter','albedo','rotation_period','bv_mag_difference','ub_mag_difference','moid']
    for column in normalize_columns:
        df_lg[column] = (df_lg[column] - df_lg[column].min()) / (df_lg[column].max() - df_lg[column].min())
    df_lg = df_lg.drop(['full_name','condition_code','spec_T', 'taxonomic_type','diameter','near_eath_object','hazard_category'], axis=1)
    return df_lg