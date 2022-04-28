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

    # Title and subtitle
    html.H1(children='Public School District Data Visualization', style={'textAlign': 'center'}),
    html.H6(children='Adolfo Calderon and Rubin McLuen', style={'textAlign': 'center'}),
    
    # Top Section
    html.Div(children=[
        html.Div(children=[
            
            # Radio Buttons
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
            
            #Slider
            html.H6('Enrollment',style={'textAlign': 'center'}),
            dcc.Slider(0, 10000,
                       marks=None,
                       value=0,
                       id='Enrollment',
                       tooltip={"placement": "bottom", "always_visible": True},
                )],style={'display': 'inline-block'}), 
        
        # Country heat map
        html.Div(children=[
            html.H6("Average Spending Per Public School Student In US Counties",style={'textAlign': 'center'}),
            dcc.Graph(id="country_map")], style={'display': 'inline-block'}),
        html.Br()],
             
        # Splitting top section into columns
        style={"display": "grid", "grid-template-columns": "14% 75% 14%"}
),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    
    #Bottom Section
    html.Div(children=[
        
        # Summary Statistics
        html.Div(children=[
            html.H2(children='Summary Statistics', style={'textAlign': 'center','font-style': 'italic'}),
            html.Div(id='district_count', style={'textAlign': 'center','font-style': 'italic', 'font-size': '25px'}),
            html.Div(id='enrollment_sum', style={'textAlign': 'center','font-style': 'italic', 'font-size': '25px'}),
            html.Div(id='spending_avg', style={'textAlign': 'center','font-style': 'italic', 'font-size': '25px'}),
            html.Div(id='poverty_rate', style={'textAlign': 'center','font-style': 'italic', 'font-size': '25px'}),
            html.Div(id='median_income', style={'textAlign': 'center','font-style': 'italic', 'font-size': '25px'}),
            html.Div(id='median_property_value', style={'textAlign': 'center','font-style': 'italic', 'font-size': '25px'}),
        ]),
        
        # State Data
        html.Div(children=[
            html.Div(children=[
                
                # Title
                html.H2(children='State Data', style={'textAlign': 'center','font-style': 'italic'}),
                
                # Dropdown menu
                dcc.Dropdown(id='state',options=[
                    {'label': 'Alabama', 'value':'AL'},
                    {'label': 'Alaska', 'value':'AK'},
                    {'label': 'Arizona', 'value':'AZ'},
                    {'label': 'Arkansas', 'value':'AR'},
                    {'label': 'California', 'value':'CA'},
                    {'label': 'Colorado', 'value':'CO'},
                    {'label': 'Connecticut', 'value':'CT'},
                    {'label': 'Delaware', 'value':'DE'},
                    {'label': 'Florida', 'value':'FL'},
                    {'label': 'Georgia', 'value':'GA'},
                    {'label': 'Hawaii', 'value':'HI'},
                    {'label': 'Idaho', 'value':'ID'},
                    {'label': 'Illinois', 'value':'IL'},
                    {'label': 'Indiana', 'value':'IN'},
                    {'label': 'Iowa', 'value':'IA'},
                    {'label': 'Kansas', 'value':'KS'},
                    {'label': 'Kentucky', 'value':'KY'},
                    {'label': 'Louisiana', 'value':'LA'},
                    {'label': 'Maine', 'value':'ME'},
                    {'label': 'Maryland', 'value':'MD'},
                    {'label': 'Massachusetts', 'value':'MA'},
                    {'label': 'Michigan', 'value':'MI'},
                    {'label': 'Minnesota', 'value':'MN'},
                    {'label': 'Mississippi', 'value':'MS'},
                    {'label': 'Missouri', 'value':'MO'},
                    {'label': 'Montana', 'value':'MT'},
                    {'label': 'Nebraska', 'value':'NE'},
                    {'label': 'Nevada', 'value':'NV'},
                    {'label': 'New Hampshire', 'value':'NH'},
                    {'label': 'New Jersey', 'value':'NJ'},
                    {'label': 'New Mexico', 'value':'NM'},
                    {'label': 'New York', 'value':'NY'},
                    {'label': 'North Carolina', 'value':'NC'},
                    {'label': 'North Dakota', 'value':'ND'},
                    {'label': 'Ohio', 'value':'OH'},
                    {'label': 'Oklahoma', 'value':'OK'},
                    {'label': 'Oregon', 'value':'OR'},
                    {'label': 'Pennsylvania', 'value':'PA'},
                    {'label': 'Rhode Island', 'value':'RI'},
                    {'label': 'South Carolina', 'value':'SC'},
                    {'label': 'South Dakota', 'value':'SD'},
                    {'label': 'Tennessee', 'value':'TN'},
                    {'label': 'Texas', 'value':'TX'},
                    {'label': 'Utah', 'value':'UT'},
                    {'label': 'Vermont', 'value':'VT'},
                    {'label': 'Virginia', 'value':'VA'},
                    {'label': 'Washington', 'value':'VI'},
                    {'label': 'West Virginia', 'value':'WA'},
                    {'label': 'Wisconsin', 'value':'WI'},
                    {'label': 'Wyoming', 'value':'WY'},
                    ],
                    placeholder="Select a State",
                    value="IA"),
                
            # State heat map
            dcc.Graph(id="state_map")])
    ]
    
)], style={"display": "grid", "grid-template-columns": "49% 49%"})])

#####################
#  Make Basic Plot  #
#####################
  
# Function takes input from radio buttons and enrollment slider
# Outputs country-wide summary statistics from that slice
@app.callback(
    Output('country_map', 'figure'),
    Output('district_count', 'children'),
    Output('spending_avg', 'children'),
    Output('poverty_rate', 'children'),
    Output('median_income', 'children'),
    Output('median_property_value', 'children'),
    Output('enrollment_sum','children'),
    Input('radioItem', 'value'),
    Input('Enrollment', 'value')
)    
def make_country_heat_map(button, enrollment):
    from urllib.request import urlopen
    import json
    import pandas as pd
    import plotly.express as px
    
    # County FIPS data
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    # Our data
    df = pd.read_csv("School_funding_viz/data/county_data.csv",dtype={"CNTY": str})
    
    # Enrollment filter
    df = df[df['Enrollment'] > enrollment]
    
    # Radio Button filters
    if button == "Predominantly White":
        df = df[df["Percent White"] >= 80]
        
    elif button == "Predominantly Nonwhite":
        df = df[df["Percent White"] <= 20]
        
    # Calculating summary statistics
    district_count = str(df[df.columns[0]].count())
    spending_avg = str(round(df["State and local revenue, per pupil, cost adjusted"].mean()))
    poverty_rate = str(round(df["Student poverty rate"].mean()))
    median_income = str(round(df["Median household income"].mean()))
    median_property_value = str(round(df["Median property value"].mean()))
    enrollment_sum = str(df["Enrollment"].sum())

    # Creating plot
    fig = px.choropleth(df, geojson=counties, locations='CNTY', color='State and local revenue, per pupil, cost adjusted',
                               color_continuous_scale="Viridis",
                               range_color=(0, 30000),
                               scope="usa",
                               labels={'State and local revenue, per pupil, cost adjusted':'Dollars ($)'},
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(title = "Spending Per Student In US Public School Districts")
    
    return fig, "Districts: " + district_count, "Average Spending Per Student: $" + spending_avg, "Poverty Rate: " + poverty_rate + "%", "Median Income: $" + median_income, "Median Property Value: $" + median_property_value, "Enrollment: " + enrollment_sum
    
# Function takes in input from drop down menu
# Outputs state heat map
@app.callback(
    Output('state_map', 'figure'),
    Input('state', 'value'),
)     
def make_state_heat_map(state):
    from urllib.request import urlopen
    import json
    import pandas as pd
    import plotly.express as px
    
    # County Data
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    # Our Data
    df = pd.read_csv("School_funding_viz/data/county_data.csv",
                       dtype={"CNTY": str})
    
    # Look only at specific state data from input
    df = df[df['STATE'] == state]

    # Make plot
    fig = px.choropleth(df, geojson=counties, locations='CNTY', color='State and local revenue, per pupil, cost adjusted',
                               color_continuous_scale="Viridis",
                               scope='usa',
                               labels={'State and local revenue, per pupil, cost adjusted':'Dollars ($)'}
                              )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
# -------------------------- MAIN ---------------------------- #


# This is the code that gets run when we call this file from the terminal
# The port number can be changed to fit your particular needs
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
