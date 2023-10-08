import dash
from dash import html
import dash_gif_component as gif
import dash_bootstrap_components as dbc


dash.register_page(__name__, 
                   path='/', 
                   name='Home',
                   title='Home',
                   image='assets/animation.png',
                   description="""
                               A guide to e-microbolity in Calgary based
                               on the 3-month pilot in summer 2019.
                               """)

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Welcome to the E-Mobility Data App!"),
            html.Hr()
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(["""
                     This project aims to assess the adoption of bicycle- and 
                     scooter-sharing programs as flexible and accessible 
                     micromobility solutions for Calgary residents, using 
                     trip data recorded during the pilot phase of the program 
                     in the summer of 2019. We also seek to identify high-traffic 
                     areas and recurring commute patterns to optimize future 
                     micromobility resource allocation.
                     """, html.Br(), html.Br(),

                     """
                     The data used in this app was sourced from the City of 
                     Calgary's Open Dataset and can be found below.
                     """,]),
            html.A("Shared Mobility Pilot Trips Dataset", 
                   href="https://data.calgary.ca/Transportation-Transit/Shared-Mobility-Pilot-Trips/jicz-mxiz",
                   target="_blank"),
            html.Div([html.Br(),
                      """
                      Fun fact: The animation below depicts the average hourly net  
                      departures (teal) and arrivals (orange) of shared vehicles in 
                      Calgary's Downtown region in the Summer of 2019. We've dubbed
                      it "Beats of the City". 
                      """,
                      html.Br(), html.Br(),
                      gif.GifPlayer(gif='assets/animation.gif', 
                                     still='assets/animation.png',
                                     autoplay=True)])
        ], width=12),
    ]),
])