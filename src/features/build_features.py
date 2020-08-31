# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 10:32:53 2020

@author: Sriram
"""

import numpy as np
from sklearn import linear_model
import pandas as pd
from scipy import signal

# we define the linear regression object
reg=linear_model.LinearRegression(fit_intercept=True)

def get_doubling_time_via_regression(in_array):
    " Use linear regression to find the doubling rate"
    y=np.array(in_array)
    X=np.arange(-1,2).reshape(-1,1)
    # for safety we are asserting that the length of the input array is 3
    assert len(in_array)==3
    reg.fit(X,y)
    intercept=reg.intercept_
    slope=reg.coef_
    return intercept/slope

def savgol_filter(df_input,column='confirmed',window=5):
    df_result=df_input
    degree=1
    # we fill the missing entries with zero
    filter_in=df_input[column].fillna(0)
    result=signal.savgol_filter(np.array(filter_in),
                        window,
                        degree)
    df_result[str(column+'_filtered')]=result
    return df_result

def rolling_reg(df_input,col='confirmed'):
    "Input is dataframe"
    "return value is a single series of doubling rates"
    days_back=3
    result=df_input[col].rolling(window=days_back,min_periods=days_back).apply(get_doubling_time_via_regression,raw=False)
    return result

def calc_filtered_data(df_input,filter_on='confirmed'):
    "Apply SavGol filter on the dataset and return the merged dataset"
    must_contain=set(['state','country',filter_on])
    assert must_contain.issubset(set(df_input.columns)),'Error in calc_filtered_data not all columns in data Frame'
    df_output=df_input.copy()
    pd_filtered_result=df_output[['state','country',filter_on]].groupby(['state','country']).apply(savgol_filter)#.reset_index()
    df_output=pd.merge(df_output,pd_filtered_result[[str(filter_on+'_filtered')]],left_index=True,right_index=True,how='left')
    
    return df_output.copy()


def calc_doubling_rate(df_input,filter_on='confirmed'):
    "Calculate doubling rate and return the dataframe"
    must_contain=set(['state','country',filter_on])
    assert must_contain.issubset(set(df_input.columns)),'Error in calc_filtered_data not all columns in data Frame'
    pd_DR_result=df_input[['state','country',filter_on]].groupby(['state','country']).apply(rolling_reg,filter_on).reset_index()
    pd_DR_result=pd_DR_result.rename(columns={filter_on:filter_on+'_DR','level_2':'index'})
    df_output=pd.merge(df_input,pd_DR_result[['index',str(filter_on+'_DR')]],left_index=True,right_on=['index'],how='left')
    df_output=df_output.drop(columns=['index'])
    return df_output


if __name__=='__main__':
    #test_data=np.array([2,4,6])
    #doubling_time=get_doubling_time_via_regression(test_data)
    #print('Test slope is :'+str(doubling_time))
    # We read the data from file
    pd_JH_data=pd.read_csv('data/processed/COVID_relational_confirmed.csv',sep=';',parse_dates=[0])
    pd_JH_data=pd_JH_data.sort_values('date',ascending=True).reset_index(drop=True).copy()
    # We process the data calculating filtered data and doubling rate
    pd_JH_result_large=calc_filtered_data(pd_JH_data)
    pd_JH_result_large=calc_doubling_rate(pd_JH_result_large)
    pd_JH_result_large=calc_doubling_rate(pd_JH_result_large,filter_on='confirmed_filtered')
    # we apply a threshold on confirmed column since if values are small doubling rate goes to infinity
    mask=pd_JH_result_large['confirmed']>100
    pd_JH_result_large['confirmed_filtered_DR']=pd_JH_result_large['confirmed_filtered_DR'].where(mask,other=np.NaN)
    pd_JH_result_large.to_csv('data/processed/COVID_final_set.csv',sep=';',index=False)
    print(pd_JH_result_large.head())