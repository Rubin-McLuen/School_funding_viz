# Good modules to have
import numpy as np, pandas as pd
import random, json, time, os

# Required Modules
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from urllib.request import urlopen

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

    html.H1(children='Super Simple Dash App!', style={'textAlign': 'center'}),
    html.H6(children='This is an example of a dash app with an interactive dashboard.'),

    html.H6("Change below to make a new figure:"),


    html.Div([
        "     Number of points for graph 1=: ",
        dcc.Input(id='new_input', value=5, type='number', debounce=True)
    ]),

    html.Div([
        "     Number of points for graph 2=: ",
        dcc.Input(id='my-input2', value=10, type='number', debounce=True)
    ]),
    html.Div([
        "     Number of points for graph 3=: ",
        dcc.Input(id='input3', value=7, type='number', debounce=True)
    ]),
    html.Div([
        "     Number of points for graph 4=: ",
        dcc.Input(id='input4', value=8, type='number', debounce=True)
    ]),

    html.Br(),

    html.Div(children=[
        dcc.Graph(id="new_figure", style={'display': 'inline-block'}),
        dcc.Graph(id='country_heat_map', style={'display': 'inline-block'}),
        dcc.Graph(id='figure3', style={'display': 'inline-block'}),

        dcc.Slider(0, 20, marks=none,
                   value=10,
                   id='my-slider'
            ),
        dcc.Graph(id='figure4', style={'display': 'inline-block'})
])
    ])


#####################
#  Make Basic Plot  #
#####################
@app.callback(
    Output('country_heat_map', 'figure'),
    Input('Button', 'value'))
def make_country_heat_map(button):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv("School_funding_viz/data/county_data.csv",
                       dtype={"CNTY": str})
    
    # df = df[df['Enrollment'] > int(enrollment)]
    
#     if button == "Predominantly White":
#         df = df[df["Percent White"] >= 80]
        
#     elif button == "Predominantly Nonwhite":
#         df = df[df["Percent White"] <= 20]
        
    district_count = df[df.columns[0]].count()
    spending_avg = round(df["State and local revenue, per pupil, cost adjusted"].mean())
    poverty_rate = round(df["Student poverty rate"].mean())
    median_income = round(df["Median household income"].mean())
    median_property_value = round(df["Median property value"].mean())
    
    # print(district_count, "/12797")
    # print(spending_avg)
    # print(poverty_rate)
    # print(median_income)
    # print(median_property_value)

    fig = px.choropleth(df, geojson=counties, locations='CNTY', color='State and local revenue, per pupil, cost adjusted',
                               color_continuous_scale="Viridis",
                               range_color=(0, 30000),
                               scope="usa",
                               labels={'State and local revenue, per pupil, cost adjusted':'Dollars $'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output('new_figure', 'figure'),
    Input("new_input", 'value'))
def make_plot2(N):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(N), y=np.random.rand(N),
                             mode='lines',
                             name='Random Data'))

    fig.update_layout(title="Graph 1")

    return fig

@app.callback(
    Output('figure4', 'figure'),
    Input("input4", 'value'))

def make_plot3(N):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(N), y=np.random.rand(N),
                             mode='lines',
                             name='Random Data'))

    fig.update_layout(title="This is the best dashboard ever")

    return fig

@app.callback(
    Output('figure3', 'figure'),
    Input("my-slider", 'value'))
def make_plot4(N):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(N), y=np.random.rand(N),
                             mode='lines',
                             name='Random Data'))

    fig.update_layout(title="Graph 3")

    return fig




# -------------------------- MAIN ---------------------------- #

# This is the code that gets run when we call this file from the terminal
# The port number can be changed to fit your particular needs
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)