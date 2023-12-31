# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='site-dropdown', options = [
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True)),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, step = 1000,
                                                marks = {0: '0',
                                                         2500 : '2500',
                                                         5000 : '5000',
                                                         7500 : '7500',
                                                         10000 : '10000'},
                                                value = [min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(value):
    filtered_df = spacex_df
    if value == 'ALL':
        fig = px.pie(spacex_df.groupby('Launch Site')['class'].count(), values = spacex_df.groupby('Launch Site')['class'].count().values, 
        names=spacex_df.groupby('Launch Site')['class'].count().index, 
        title='Total Success Launches by Site')
        return fig
    elif value == "CCAFS LC-40":
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        fig = px.pie(filtered_df.groupby('class')['class'].count(), values = 'class', 
        names= filtered_df.groupby('class')['class'].count().index, 
        title='Total Success Launches for Site CCAFS LC-40')
        return fig
    elif value == "VAFB SLC-4E":
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        fig = px.pie(filtered_df.groupby('class')['class'].count(), values = 'class', 
        names= filtered_df.groupby('class')['class'].count().index, 
        title='Total Success Launches for Site VAFB SLC-4E')
        return fig
    elif value == "KSC LC-39A":
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        fig = px.pie(filtered_df.groupby('class')['class'].count(), values = 'class', 
        names= filtered_df.groupby('class')['class'].count().index, 
        title='Total Success Launches for Site KSC LC-39A')
        return fig
    elif value == "CCAFS SLC-40":
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        fig = px.pie(filtered_df.groupby('class')['class'].count(), values = 'class', 
        names= filtered_df.groupby('class')['class'].count().index, 
        title='Total Success Launches for Site CCAFS SLC-40')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(value, slider):
    filtered_df = spacex_df
    if value == "ALL":
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= slider[0]) & (spacex_df['Payload Mass (kg)'] <= slider[1])] 
        fig = px.scatter(filtered_df, x = "Payload Mass (kg)", y = 'class', color = 'Booster Version Category', 
                         title= 'Correlation Between Payload and Success for All Sites')
        return fig
    elif value == "CCAFS LC-40":
        filtered_df = spacex_df[(spacex_df['Launch Site'] == 'CCAFS LC-40') & ((spacex_df['Payload Mass (kg)'] >= slider[0]) & (spacex_df['Payload Mass (kg)'] <= slider[1]))] 
        fig = px.scatter(filtered_df, x = "Payload Mass (kg)", y = 'class', color = 'Booster Version Category', 
                         title= 'Correlation Between Payload and Success for Site CCAFS LC-40')
        return fig
    elif value == "VAFB SLC-4E":
        filtered_df = spacex_df[(spacex_df['Launch Site'] == 'VAFB SLC-4E') & ((spacex_df['Payload Mass (kg)'] >= slider[0]) & (spacex_df['Payload Mass (kg)'] <= slider[1]))] 
        fig = px.scatter(filtered_df, x = "Payload Mass (kg)", y = 'class', color = 'Booster Version Category', 
                         title= 'Correlation Between Payload and Success for Site VAFB SLC-4E')
        return fig
    elif value == "KSC LC-39A":
        filtered_df = spacex_df[(spacex_df['Launch Site'] == 'KSC LC-39A') & ((spacex_df['Payload Mass (kg)'] >= slider[0]) & (spacex_df['Payload Mass (kg)'] <= slider[1]))] 
        fig = px.scatter(filtered_df, x = "Payload Mass (kg)", y = 'class', color = 'Booster Version Category', 
                         title= 'Correlation Between Payload and Success for Site KSC LC-39A')
        return fig
    elif value == "CCAFS SLC-40":
        filtered_df = spacex_df[(spacex_df['Launch Site'] == 'CCAFS SLC-40') & ((spacex_df['Payload Mass (kg)'] >= slider[0]) & (spacex_df['Payload Mass (kg)'] <= slider[1]))] 
        fig = px.scatter(filtered_df, x = "Payload Mass (kg)", y = 'class', color = 'Booster Version Category', 
                         title= 'Correlation Between Payload and Success for Site CCAFS SLC-40')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
