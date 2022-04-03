from dash import dcc
from dash import html
import dash_daq as daq

# Configure knob gradient used in dashboard_layout()
knob_scale={
        'gradient':True,
        'ranges':{
            'green':[0,5],
            'yellow':[5,9],
            'red':[9,10]
        }
    }

def dashboard_layout(dash_app):
    """Creates the dashboard layout with the given dash_app."""
    dash_app.layout = html.Div(className='container', children=[
        html.H1(children="Wisconsin IoHT Dashboard"),
        dcc.Dropdown(
            options=[
                {
                    'label': 'OURA Data',
                    'value': 'oura'
                },
                {
                    'label': 'Symptom Input',
                    'value': 'input'
                },
                {
                    'label': 'Schedule Selector',
                    'value': 'schedule'
                }
            ]
        ),
        daq.Knob(
            label = 'Test',
            value = 10,
            color = knob_scale
        )
    ])