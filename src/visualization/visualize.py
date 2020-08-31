# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:00:40 2020

@author: Sriram
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

df_input_large=pd.read_csv('data/processed/COVID_final_set.csv',sep=';')

fig=go.Figure()
app=dash.Dash()
app.layout=html.Div([
        dcc.Markdown('''
                     # Applied Datascience on COVID-19 Data
                     Goal of the project is to create a responsive Dashboard 
                     with data from many countries in an automated way through:
                    data gathering , data transformation,
                    filtering and machine learning to approximate doubling time.
                    '''),
        # For Country dropdown menu
        dcc.Markdown(''' ## Multi-Select Country for Visualization'''),
        
        dcc.Dropdown( id='country_drop_down',
                     options=[{'label':each,'value':each} for each in df_input_large['country'].unique()],
                     value=['Germany','India','US'],
                     multi=True),
        # For Doubling rate or conformed cased drop down mneu
        dcc.Markdown(''' ## Select Timeline of confirmed COVID-19 cases or approximated doubling time'''),
        
        dcc.Dropdown( id='doubling_time',
                     options=[
                             {'label':'Timeline Confirmed','value':'confirmed'},
                             {'label':'Timeline Confirmed Filtered','value':'confirmed_filtered'},
                             {'label':'Timeline Doubling Rate','value':'confirmed_DR'},
                             {'label':'Timeline Doubling Rate Filtered','value':'confirmed_filtered_DR'},
                             ],
                     value='confirmed',
                     multi=False),
        dcc.Graph(figure=fig,id='main_window_slope')
        
                    ])

@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value')])
def update_figure(country_list,show_doubling):
    if 'DR' in show_doubling:
        my_yaxis={'type':"log",
               'title':'Approximated doubling rate over 3 days'
                 }
    else:
        my_yaxis={'type':"log",
                  'title':'Confirmed infected people (source: johns hopkins csse, log-scale)'
                 }
    #Define the traces for the countries
    traces = []
    for each in country_list:
        df_plot=df_input_large[df_input_large['country']==each]
        if show_doubling=='confirmed_filtered_DR':
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.sum).reset_index()
       
        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                    )

    return {'data':traces,
            'layout':dict(
                width=1280,
                height=600,
                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f")},
                yaxis=my_yaxis)
            }

if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False)