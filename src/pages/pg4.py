import pandas as pd
import pathlib
import plotly.express as px

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, 
                   path='/duration-distance',
                   name='Trip Duration & Distance Analyses',
                   title='Trip Duration & Distance')


# loading the trip data and transforming it accordingly
def get_pandas_data(csv_filename: str) -> pd.DataFrame:
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath("../data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(csv_filename))

df1 = get_pandas_data("df5.csv")
df2 = get_pandas_data("df6.csv")

# Figure 1 - Trip Duration Time Series
# drop scooter record for july third because it's an outlier
fig1 = px.line(df1,
               x="start_date",
               y="trip_duration",
               color="vehicle_type",
               color_discrete_map={'bicycle':'#636EFA', 
                                   'scooter':'#EF553B'},
               title='Trip Duration Analyses by Date',
               markers=True,
               height=500,
               width=1000,
               ).update_layout(
                   xaxis={'rangeslider_visible':True},
                   xaxis_title="Trip Date", 
                   yaxis_title="Median Trip Duration (Minutes)",
        )

fig1.update_layout(legend=dict(title= "Vehicle Type"),)


# Figure 2 - Trip Duration Analysis
# drop scooter record for july third because it's an outlier
fig2 = px.line(df2,
               x="start_date",
               y="trip_distance",
               color="vehicle_type",
               color_discrete_map={'bicycle':'#636EFA', 
                                   'scooter':'#EF553B'},
               title='Trip Distance Analyses by Date',                    
               markers=True,
               height=500,
               width=1000,
               ).update_layout(
                   xaxis={'rangeslider_visible':True},
                   xaxis_title="Trip Date", 
                   yaxis_title="Median Distance Traveled (Kilometers)",
                   )
fig2.update_layout(legend=dict(title= "Vehicle Type"),)


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3(children="Trip Duration & Distance Analyses", 
                    style={'textAlign':'left'}),
            html.Hr()
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig1, id='graph-1')
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig2, id='graph-2')
        ], width=12)
    ])
])