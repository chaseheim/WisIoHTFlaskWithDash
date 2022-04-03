from dash import dcc
from dash import html
from dash.dependencies import Input, Output
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

def register_layout(dash_app):
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
            id='test-knob',
            label = 'Test',
            value = 0,
            color = knob_scale
        ),
        html.Div(id='knob-output'),
        daq.BooleanSwitch(
            on=False,
            label='Cough',
            labelPosition='top'
        ),
        daq.BooleanSwitch(
            on=False,
            label='Fever',
            labelPosition='top'
        ),
        daq.BooleanSwitch(
            on=False,
            label='Sore Throat',
            labelPosition='top'
        ),
        daq.BooleanSwitch(
            on=False,
            label='Shortness of breath',
            labelPosition='top'
        ),
        daq.BooleanSwitch(
            on=False,
            label='Head Ache',
            labelPosition='top'
        ),
        daq.BooleanSwitch(
            on=False,
            label='Test indication',
            labelPosition='top'
        )
    ])

def init_callbacks(dash_app):
    @dash_app.callback(
        # Callback inputs and outputs
        Output('knob-output', 'children'),
        Input('test-knob', 'value')
    )
    def update_knob_output(value):
        return 'Knob value is {}'.format(value)