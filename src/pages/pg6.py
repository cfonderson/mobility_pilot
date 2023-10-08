import pandas as pd
import pathlib
import plotly.express as px

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, 
                   path='/geo-animation',
                   name='Animated Geoplot',
                   title='Animated Geoplot')

# loading the trip data and transforming it accordingly
def get_pandas_data(csv_filename: str) -> pd.DataFrame:
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath("../data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(csv_filename))

df = get_pandas_data("df10.csv")

# Figure
fig = px.scatter_mapbox(
    df,
    lat='starty',
    lon='startx',
    color='daily_avg', 
    animation_frame='start_hour',
    size='counts',
    size_max=45,
    color_continuous_scale='IceFire',
    range_color=[0, 10],
    mapbox_style='carto-positron',
    center={'lat':51.0456333,
            'lon':-114.0691622},
    custom_data=['starting_grid_id', 
                'counts', 
                'daily_avg'],
    zoom=13,
    height=850
)

fig.update_layout(
    updatemenus=[dict(
        direction='up',
        buttons=list([
            dict(label='Play'),
            dict(label='Pause'),
        ])
    )],
    sliders=[{'currentvalue': {'prefix': 'Time of day: ',
                               'xanchor':'right'},
    }],
    coloraxis_colorbar={
        'title':"Daily Count",
    },
)

hover = "Grid ID: " + df['starting_grid_id'] + "<br>" + \
                    "Total Counts: " +  df['counts'].astype('str') +"</br>" + \
                    "Daily Count (Mean): " + df['daily_avg'].astype('str')

fig.update_traces(hovertemplate=hover)
for frame in fig.frames:
    frame.data[0].hovertemplate = hover


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Breakdown of Trip Counts by Hour of Day and Location", 
                    style={'textAlign':'left'}),
            html.Hr(),
            html.P("""
                   Below is an interactive version of the animated GIF on our 
                   home page, depicting the frequency of trips taken downtown
                   Calgary throughout the ride sharing pilot of 2019. The total
                   count by location has been averaged over the length of the 
                   pilot (91 days) to yield a mean daily trip count for each 
                   grid and hour of the day.
                   """)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig, id='graph')
        ], width=12)
    ])
])