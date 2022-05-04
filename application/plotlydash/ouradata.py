from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.graph_objects as go
from dash import html
from application import oauth
from flask import session
from datetime import datetime
from dateutil import tz
import numpy as np

def smoothTriangle(data, degree):
    triangle=np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1])) # up then down
    smoothed=[]

    for i in range(degree, len(data) - degree * 2):
        point=data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point)/np.sum(triangle))
    # Handle boundaries
    smoothed=[smoothed[0]]*int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed

heartrate_card = dbc.Card(
    [
        dbc.CardHeader('Oura Data'),
        dbc.CardBody(
            [
                html.H5(className='card-title', children='Sync Oura Data'),
                html.H6(className='card-subtitle mb2 text-muted', children='Sync your oura data and view it below'),
                # Sync Oura Data
                dbc.Button("Sync Data", color="primary", id='oura-sync-btn', n_clicks=0, class_name='mt-2 mb-2'),
                                    
                dcc.Graph(id='heartrate'),
                dbc.Label('Moving Average (Less or more smoothing)', html_for='slider_average'),
                dcc.Slider(id='slider_average', min=1, max=10, step=1, value=10),
            ]
        )
    ],
),

container = html.Div(
    heartrate_card,
    className='pt-3'
)

def get_oura_layout():
    return container

def get_oura_data(n_clicks, average):
    figure = {
            'data': [],
            'layout': {
                'title': 'Heartrate of Past 24 Hours'
            }
        }

    if n_clicks > 0:
        # Get provider from oauthlib
        oura = oauth.create_client('oura')
        # Get token from session TODO: Dont do this use RDS instead (Better yet make a function with oauthlib that does this for us and we just call the function)
        token = session.get('demo_token')
        print("TOKEN FROM SESSION: " + str(token))
        
        # Get oura data for heartrate
        response = oura.get('heartrate', token=token)
        # TODO: Actually check we got the data, this would break the application if it threw and error and uncommented
        #response.raise_for_status()
        # TODO: Check that data exists, if we succeed in getting data, but that data is blank it will also break: {'data': [], 'next_token': None}
        # TODO: Store data in a dash.store object. This way we dont have to ask Oura every time for the same data. Check if it exists in storage or not and react accordingly

        data = response.json()
        print(data)

        timestamp = []
        heartrate = []

        for n in range(len(data['data'])):
            heartrate.append(data['data'][n]['bpm'])
            UTCtime = data['data'][n]['timestamp']
            
            # Format time from UTC to CST
            # TODO: Add settings for timezone, get from session
            to_zone = tz.gettz('America/Chicago')
            utc = datetime.strptime(UTCtime, '%Y-%m-%dT%H:%M:%S+00:00')
            utc = utc.replace(tzinfo=tz.gettz('UTC'))
            new_time = utc.astimezone(to_zone)
            timestamp.append(new_time)
        
        figure = go.Figure(data=[go.Scatter(x=timestamp, y=smoothTriangle(heartrate, average), line_shape='linear', name="Average Heartrate")])
        figure.add_trace(go.Scatter(
            x=timestamp,
            y=heartrate,
            mode='markers',
            marker=dict(
                size=3,
                color='black',
                symbol='circle-open'
            ),
            name='Raw Heartrate'
        ))

    return figure