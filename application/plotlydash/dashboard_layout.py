from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from .symptominput import get_symptom_form, get_symptom_submit
from application import oauth
from flask import session
from requests.exceptions import HTTPError
import pandas as pd

def register_layout(dash_app):
    """Creates the dashboard layout with the given dash_app."""
    dash_app.layout = html.Div(id='layout', children=
        [
            get_symptom_form(),

            # Display Oura Data
            html.Div(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader('Oura Data'),
                            dbc.CardBody(
                                [
                                    html.H5(className='card-title', children='Sync Oura Data'),
                                    html.H6(className='card-subtitle mb2 text-muted', children='Sync your oura data and view it below'),
                                    # Sync Oura Data
                                    dbc.Button("Sync Data", color="primary", id='oura-sync-btn', n_clicks=0, class_name='mt-2 mb-2'),
                                    
                                    dcc.Graph(id='heartrate'),
                                ]
                            )
                        ],
                    ),
                ],
                className='pt-3'
            ),

            #dcc.Store stores oura information
            dcc.Store(id='oura-store'),
        ]
    )

def init_callbacks(dash_app):
    @dash_app.callback(
        Output('symptom-alert', 'is_open'),
        Output('percent-covid', 'value'),
        Input('symptom-submit', 'n_clicks'),
        Input('checkbox_cough', 'value'),
        Input('checkbox_fever', 'value'),
        Input('checkbox_sore_throat', 'value'),
        Input('checkbox_shortness_of_breath', 'value'),
        Input('checkbox_head_ache', 'value'),
        Input('checkbox_test_indication', 'value'),
        Input('slider_feeling', 'value'),
    )
    def symptom_submit(n_clicks, cough, fever, throat, breath, ache, test, slider):
        (is_open, percent) = get_symptom_submit(n_clicks, cough, fever, throat, breath, ache, test, slider)
        n_clicks = n_clicks + 100
        return is_open, int(percent)

    @dash_app.callback(Output('heartrate', 'figure'), Input('oura-sync-btn', 'n_clicks'))
    def sync_oura_data(n_clicks):
        figure = ''

        if n_clicks == 1:
            oura = oauth.create_client('oura')
            token = session.get('demo_token')
            print("TOKEN FROM SESSION: " + str(token))
            
            response = oura.get('heartrate', token=token)
            response.raise_for_status()
            data = response.json()
            #data = response.json()['data']
            #data = pd.DataFrame(data)
            print(data)

            # Format data
            figure = {
                'data': [],
                'layout': {
                    'title': 'Heartrate of Past 24 Hours'
                }
            }

            for n in range(101):
                heartrate = data['data'][n]['bpm']
                timestamp = data['data'][n]['timestamp']
                temp = {'x': [n], 'y': [heartrate], 'type': 'bar', 'name': '{}'.format(timestamp)}
                figure['data'].append(temp)

        return figure