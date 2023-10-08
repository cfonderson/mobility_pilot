import pandas as pd
import pathlib
import plotly.express as px

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, 
                   path='/trip-frequency',
                   name='Trip Frequency Analyses',
                   title='Frequency Analyses')


# loading the trip data and transforming it accordingly
def get_pandas_data(csv_filename: str) -> pd.DataFrame:
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath("../data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(csv_filename))

# Data
df1 = get_pandas_data("df2.csv")
df1.start_date = pd.to_datetime(df1.start_date)

df2 = get_pandas_data("df3.csv")
df2.start_date = pd.to_datetime(df2.start_date)

df3 = get_pandas_data("df4.csv")
df3.start_date = pd.to_datetime(df3.start_date).dt.strftime('%Y-%m-%d')


# Figure 1 - Trip Count by Days
fig1 = px.bar(df1, 
              x="start_date",
              y="count",
              labels={'start_date':'Date'}, 
              title='Trip Frequency by Vehicle Type: July to September 2019',
              color="vehicle_type",
              color_discrete_sequence=['darkgoldenrod', 'orange'],
             )

fig1.update_layout(legend=dict(title= "Vehicle Type"),
                   yaxis_tickformat = '000',
                   yaxis_title="Number of Trips",)

fig1.add_vrect(x0="2019-07-01", x1="2019-08-01",
               fillcolor="lightgreen", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="July", annotation_position="top left"
              ),
fig1.add_vrect(x0="2019-08-01", x1="2019-09-01",
               fillcolor="yellowgreen", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="August", annotation_position="top left"
              ),
fig1.add_vrect(x0="2019-09-01", x1="2019-09-30",
               fillcolor="yellow", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="September", annotation_position="top left"
              )


# Figure 2 - Trip Count by Weekday Category
fig2 = px.bar(df2, 
              x="start_date",
              y="count",
              title='Trip Frequency by Day Category: July to September 2019',
              labels={'start_date':'Date'}, 
              color = 'day_cat',
              color_discrete_map={'Weekday':'darkorange',
                                  'Weekend':'darkcyan'}
             )

fig2.update_layout(legend=dict(title= "Day Category"),
                   yaxis_tickformat = '000',
                   yaxis_title="Number of Trips",)

fig2.add_vrect(x0="2019-07-01", x1="2019-08-01",
               fillcolor="lightgreen", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="July", annotation_position="top left"
              ),
fig2.add_vrect(x0="2019-08-01", x1="2019-09-01",
               fillcolor="yellowgreen", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="August", annotation_position="top left"
              ),
fig2.add_vrect(x0="2019-09-01", x1="2019-09-30",
               fillcolor="yellow", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="September", annotation_position="top left"
              )

# Figure 3 - Trip Counts by Date (with Festivals)
default_color = "darkorange"
colors = {"2019-09-21": "gold", "2019-09-14":"silver","2019-09-13":"chocolate"} #Peak days 

color_discrete_map = {
    c: colors.get(c, default_color) 
    for c in df3.start_date.unique()}


fig3 = px.bar(df3, 
              x="start_date",
              y="count",
              title='Trip Frequency by Summer Event: July to September 2019',
              labels={'start_date':'Date'}, 
              color = 'start_date',
              color_discrete_map=color_discrete_map,
            )

fig3.update_layout(yaxis_title="Number of Trips",
                   yaxis_tickformat = '000',
                   showlegend=False)

# Major events
fig3.add_vrect(x0="2019-07-05", x1="2019-07-14", 
               fillcolor="olive", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="Stampede", annotation_position="top left"
              ),
fig3.add_vrect(x0="2019-07-25", x1="2019-07-28",
               fillcolor="olive", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="Folk Fest", annotation_position="top left"
              ),
fig3.add_vrect(x0="2019-08-08", x1="2019-08-11",
               fillcolor="olive", opacity=0.25,
               layer="below", line_width=0,
               annotation_text="Taste of Calgary", annotation_position="top left"
              )

# Annotate peak days
fig3.add_annotation(x='2019-09-13',
                    y= 9200,
                    ax=-30,
                    ay=-30,
                    text="",
                    showarrow=True,
                    arrowhead=1)
fig3.add_annotation(x='2019-09-14', 
                    y= 9200,
                    ax=30,
                    ay=-30,
                    text="",
                    showarrow=True,
                    arrowhead=1)
fig3.add_annotation(x='2019-09-21', 
                    y= 9200,
                    ax=30,
                    ay=-30,
                    text="",
                    showarrow=True,
                    arrowhead=1)
fig3.add_annotation(text="Highest Number of Trips Made",
                  xref="paper", yref="paper",
                  x=0.95, y=1.02, showarrow=False)



layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3(children="Trip Frequency Analyses", 
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
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig3, id='graph-3')
        ], width=12)
    ])
])