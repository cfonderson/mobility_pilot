import numpy as np
import pandas as pd
import pathlib
import plotly.graph_objects as go

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, 
                   path='/periods',
                   name='Periodic Breakdown',
                   title='Periodic Breakdown')


# loading the trip data array
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
with open(DATA_PATH.joinpath('arrays.npy'), 'rb') as f:
    arrays = np.load(f)


# Figure
fig = go.Figure(
    data=[go.Heatmap(z=arrays[0],
                     y=['Sunday', 'Monday', 'Tuesday', 
                        'Wednesday', 'Thursday', 'Friday', 
                        'Saturday'],
                    )],

    layout=go.Layout(
        title="Hourly Breakdown of Average Trip Counts by Weekday and Month",
        updatemenus=[dict(
            type="buttons",
            direction="right",
            active=0,
            showactive=True,
            x=1.0, y=1.15,
            buttons=[dict(label="Entire Pilot",
                          method="update",
                          args=[{'z':[arrays[0]]}]),
                     dict(label="July",
                          method="update",
                          args=[{'z':[arrays[1]]}]),
                     dict(label="August",
                          method="update",
                          args=[{'z':[arrays[2]]}]),
                     dict(label="September",
                          method="update",
                          args=[{'z':[arrays[3]]}])])]
    ),
)

fig.update_layout(
    yaxis={"autorange": "reversed",
           "tickmode": "array",
           "ticktext": ['One', 'Three', 'Five', 'Seven', 'Nine', 'Eleven']},
    xaxis={"dtick": 1},
    xaxis_title="Time of day", 
    yaxis_title="Week day"
)


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3(children="Trip Frequency by Time Periods", 
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