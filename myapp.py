# Good modules to have
import numpy as np, pandas as pd
import random, json, time, os

# Required Modules
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Add basic CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# This is the main application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Do not bother us with exceptions
app.config.suppress_callback_exceptions = True

#################################################
################# Layout ########################
#################################################
app.layout = html.Div([

    
    html.H1(children='Public School District Data Visualization', style={'textAlign': 'center'}),
    html.H6(children='Adolfo Calderon and Rubin McLuen', style={'textAlign': 'center'}),
    
    html.Div(children=[
        html.Div(children=[
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.RadioItems(
                id='radioItem',
                options=[
                       {'label': 'All', 'value':'All'},
                       {'label': 'Predominantly White', 'value': 'Predominantly White'},
                       {'label': 'Predominantly Nonwhite', 'value': 'Predominantly Nonwhite'},
                   ],
                   value='All'),
            html.H6('Enrollment',style={'textAlign': 'center'}),
            dcc.Slider(0, 10000,
                       marks=None,
                       value=0,
                       id='Enrollment',
                       tooltip={"placement": "bottom", "always_visible": True},
                )],style={'display': 'inline-block'}), 
        html.Div(children=[
            html.H6("Average Spending Per Public School Student In US Counties",style={'textAlign': 'center'}),
            dcc.Graph(id="country_map")], style={'display': 'inline-block'}),
        html.Br()],
             
        style={"display": "grid", "grid-template-columns": "14% 75% 14%"}
),
    html.Div(children=[
        html.H2(children='Summary Statistics', style={'textAlign': 'center','font-style': 'italic'}),
        html.Div(children=[
            html.H2(children='State Data', style={'textAlign': 'center','font-style': 'italic'}),
            dcc.Input(id='state', value="IA", type='number', debounce=True),
            dcc.Graph(id="state_map")])
    ],
             
        style={"display": "grid", "grid-template-columns": " 50% 50%"})
    
])

#####################
#  Make Basic Plot  #
#####################
    
@app.callback(
    Output('country_map', 'figure'),
    Input('radioItem', 'value'),
    Input('Enrollment', 'value')
)    
def make_country_heat_map(button, enrollment):
    from urllib.request import urlopen
    import json
    import pandas as pd
    import plotly.express as px
    
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv("School_funding_viz/data/county_data.csv",dtype={"CNTY": str})
    
    df = df[df['Enrollment'] > enrollment]
    
    if button == "Predominantly White":
        df = df[df["Percent White"] >= 80]
        
    elif button == "Predominantly Nonwhite":
        df = df[df["Percent White"] <= 20]
        
    district_count = df[df.columns[0]].count()
    spending_avg = round(df["State and local revenue, per pupil, cost adjusted"].mean())
    poverty_rate = round(df["Student poverty rate"].mean())
    median_income = round(df["Median household income"].mean())
    median_property_value = round(df["Median property value"].mean())
    
    print(district_count, "/12797")
    print(spending_avg)
    print(poverty_rate)
    print(median_income)
    print(median_property_value)

    fig = px.choropleth(df, geojson=counties, locations='CNTY', color='State and local revenue, per pupil, cost adjusted',
                               color_continuous_scale="Viridis",
                               range_color=(0, 30000),
                               scope="usa",
                               labels={'State and local revenue, per pupil, cost adjusted':'Dollars ($)'},
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(title = "Spending Per Student In US Public School Districts")
    
    return fig
    
    
@app.callback(
    Output('state_map', 'figure'),
    Input('state', 'value'),
)     
def make_state_heat_map(state):
    from urllib.request import urlopen
    import json
    import pandas as pd
    import plotly.express as px
    
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv("School_funding_viz/data/county_data.csv",
                       dtype={"CNTY": str})
    
    df = df[df['STATE'] == state]
    district_count = df[df.columns[0]].count()
    spending_avg = round(df["State and local revenue, per pupil, cost adjusted"].mean())
    poverty_rate = round(df["Student poverty rate"].mean())
    median_income = round(df["Median household income"].mean())
    median_property_value = round(df["Median property value"].mean())
    
    print(district_count)
    print(spending_avg)
    print(poverty_rate)
    print(median_income)
    print(median_property_value)
    
    fig = px.choropleth(df, geojson=counties, locations='CNTY', color='State and local revenue, per pupil, cost adjusted',
                               color_continuous_scale="Viridis",
                               scope='usa',
                               labels={'State and local revenue, per pupil, cost adjusted':'Dollars $'}
                              )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
# -------------------------- MAIN ---------------------------- #


# This is the code that gets run when we call this file from the terminal
# The port number can be changed to fit your particular needs
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
