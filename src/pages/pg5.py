import pandas as pd
import pathlib
import plotly.graph_objects as go

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, 
                   path='/geomapping',
                   name='Geomapping Analyses',
                   title='Geomapping Analyses')


# loading the trip data and transforming it accordingly
def get_pandas_data(csv_filename: str) -> pd.DataFrame:
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath("../data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(csv_filename))

df1 = get_pandas_data("df8.csv")
df1['counts_str'] = df1['counts_str'].astype('str')
df2 = get_pandas_data("df9.csv")
df2['counts_str'] = df2['counts_str'].astype('str')

# Figure
fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    lat=df1["starty"], 
    lon=df1["startx"], 
    mode='markers', 
    marker=go.scattermapbox.Marker(
        size=df1["total_count"]/100,
        color="#FF9900",
    ),
    text="Grid ID: " + df1["starting_grid_id"] + "<br>" + \
         "Popularity: " + df1["frequency"] + "<br>" + \
         "Trip Counts: " + df1["counts_str"],
    hoverinfo='text',
    name="Departures"
    ), )

fig.add_trace(go.Scattermapbox(
    lat=df2["endy"], 
    lon=df2["endx"], 
    mode='markers', 
    marker=go.scattermapbox.Marker(
        size=df2["total_count"]/100,
        color="#17BCEF",
    ),
    text="Grid ID: " + df2["ending_grid_id"]+ "<br>" + \
         "Popularity: " + df2["frequency"] + "<br>" + \
         "Trip Counts: " + df2["counts_str"],
    hoverinfo='text',
    name="Arrivals"
))

# add buttons to change layout
fig.update_layout(
    title='Trip Frequencies by Location',
    showlegend=False, 
    autosize=True,
    height=800,
    hovermode='closest',
    mapbox=dict(
        style="carto-positron",
        bearing=0,
        center=dict( 
            lat=51.0456360,
            lon=-114.0691622),
        pitch=0, 
        zoom=13,
    ),
    updatemenus = [
        dict(
            active=0,
            type='buttons',
            direction="right",
            showactive=True,
            x=1.0, y=1.07,
            buttons=list([   
                dict(label ='All Trips',
                     method = 'update',
                     args = [{'visible': [True, True]},]),
                dict(label = 'Departures',
                    method = 'update',
                    args = [{'visible': [True, False]},]),
                dict(label = 'Arrivals',
                    method = 'update',
                    args = [{'visible': [False, True]},])
            ]),
        )
    ],    
)


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Hourly Average Number of Trips Centered Around Downtown Calgary", 
                    style={'textAlign':'left'}),
            html.Hr()
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig, id='graph')
        ], width=12)
    ])
])