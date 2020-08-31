# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 12:22:53 2020

@author: Sriram
"""
import pandas as pd
import requests
import subprocess
import os
import numpy as np
from datetime import datetime


def store_flat_table_JH_data():
    "process raw JH data into a flat table data structure"
    datapath='data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    JH_data_raw=pd.read_csv(datapath)
    time_index=JH_data_raw.columns[4:]
    pd_flat_table=pd.DataFrame({'date':time_index})
    country_list=JH_data_raw['Country/Region'].unique()
    for country in country_list:
        pd_flat_table[country]=np.array(JH_data_raw[JH_data_raw['Country/Region']==country].iloc[:,4::].sum(axis=0))
    time_index=[datetime.strptime(each,"%m/%d/%y") for each in pd_flat_table.date]
    pd_flat_table['date']=time_index
    pd_flat_table.to_csv('data/processed/COVID_JH_flat_table_confirmed.csv',sep=';',index=False )
    print('Latest date is'+str(max(pd_flat_table.date)))
    print(' Number of rows stored: '+str(pd_flat_table.shape[0]))

#running the function
if __name__ == '__main__':
    store_flat_table_JH_data()