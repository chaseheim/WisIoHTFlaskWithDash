from dash import html
from dash.dependencies import Input, Output
from .symptominput import get_symptom_form, get_symptom_submit

def register_layout(dash_app):
    """Creates the dashboard layout with the given dash_app."""
    dash_app.layout = html.Div(id='symptom-input', children=
        [
            get_symptom_form(),
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