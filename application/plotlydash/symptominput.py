from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc
from dash import html
import lightgbm as lgb
import pandas as pd

symptom_input = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Label('Cough', html_for='checkbox_cough'),
                dbc.Checkbox(id='checkbox_cough', value=False),
            ]
        ),
        dbc.Col(
            [
                dbc.Label('Fever', html_for='checkbox_Fever'),
                dbc.Checkbox(id='checkbox_fever', value=False),
            ]
        ),
        dbc.Col(
            [
                dbc.Label('Sore Throat', html_for='checkbox_sore_throat'),
                dbc.Checkbox(id='checkbox_sore_throat', value=False),
            ]
        ),
        dbc.Col(
            [
                dbc.Label('Shortness of Breath', html_for='checkbox_shortness_of_breath'),
                dbc.Checkbox(id='checkbox_shortness_of_breath', value=False),
            ]
        ),
        dbc.Col(
            [
                dbc.Label('Head Ache', html_for='checkbox_head_ache'),
                dbc.Checkbox(id='checkbox_head_ache', value=False),
            ]
        ),
        dbc.Col(
            [
                dbc.Label('Test Indication', html_for='checkbox_test_indication'),
                dbc.Checkbox(id='checkbox_test_indication', value=False),
            ]
        ),
    ]
)

symptom_slider = dbc.Row(
    [
        dbc.Label('How are you feeling? (10 being excellent)', html_for='slider_feeling'),
        dcc.Slider(id='slider_feeling', min=0, max=10, step=1, value=10),
    ],
    class_name="mb-3",
)

result = dbc.Row(
    [
        daq.Gauge(
            showCurrentValue=True,
            units="%",
            value=0,
            max=100,
            min=0,
            label='Percent chance you have COVID-19:',
            id='percent-covid',
            color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
        )
    ],
)

input_card = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader('Symptom Input'),
                dbc.CardBody(
                    [
                        dbc.Alert(['Submission recieved!'], id='symptom-alert', color="success", dismissable=True, is_open=False),
                        html.H5(className='card-title', children='COVID-19 Symptom Input'),
                        html.H6(className='card-subtitle mb2 text-muted', children='Input the current symptoms you are experiencing'),
                        dbc.Form([symptom_input, symptom_slider,]),
                        dbc.Button("Submit", color="primary", id='symptom-submit', n_clicks=0),
                    ]
                )
            ]
        ),
    ]
)

output_card = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader('Symptom Output'),
                dbc.CardBody(
                    [
                        html.H5(className='card-title', children='COVID-19 Symptom Output'),
                        html.H6(className='card-subtitle mb2 text-muted', children='Output from the symptom data you provided above'),
                        result,
                    ]
                )
            ]
        ),
    ],
    className='pt-3'
)

container = html.Div(
    [input_card, output_card]
)

def get_symptom_form():
    return container

def get_symptom_submit(n_clicks, cough, fever, throat, breath, ache, test, slider):
    if n_clicks == 0:
        return (False, 0)

    if n_clicks == 1:
        data = {
            'cough': [int(cough)],
            'fever': [int(fever)],
            'sore_throat': [int(throat)],
            'shortness_of_breath': [int(breath)],
            'head_ache': [int(ache)],
            'gender': [int('1')],
            'test_indication': [int(test)],
            'age_60_and_above': [int('0')]
        }

        # Run submission through ML algorithm and return percentage
        data = pd.DataFrame(data)
        bst = lgb.Booster(model_file='model.txt')
        ypred1=bst.predict(data)
        is_open = True
        return (is_open, (ypred1 * 100))

    if n_clicks >= 2:
        return(False, 0)
