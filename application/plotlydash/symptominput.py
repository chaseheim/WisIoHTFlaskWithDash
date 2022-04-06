from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

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

card_container = dbc.Card(
    [
        dbc.CardHeader('Symptom Input'),
        dbc.CardBody(
            [
                dbc.Alert(['Submition recieved!'], id='symptom-alert', color="success", dismissable=True, is_open=False),
                html.H5(className='card-title', children='COVID-19 Symptom Input'),
                html.H6(className='card-subtitle mb2 text-muted', children='Input the current symptoms you are experiencing'),
                dbc.Form([symptom_input, symptom_slider,]),
                dbc.Button("Submit", color="primary", id='symptom-submit', n_clicks=0),
            ]
        )
    ]
)

def get_symptom_form():
    return card_container

def get_symptom_submit(n_clicks, cough, fever, throat, breath, ache, test, slider):
    # Example data: {'cough': False, 'fever': True, 'throat': False, 'breath': False, 'ache': False, 'test': False, 'slider': 2}
    data = {
        'cough': cough,
        'fever': fever,
        'throat': throat,
        'breath': breath,
        'ache': ache,
        'test': test,
        'feeling_slider': slider,
    }
    if n_clicks == 1:
        print("SUBMITION RECIEVED")
        print(data)
        n_clicks = n_clicks + 1
        return True
