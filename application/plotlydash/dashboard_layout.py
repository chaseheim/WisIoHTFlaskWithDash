from dash import html
from dash.dependencies import Input, Output
from .symptominput import get_symptom_layout, get_symptom_submit
from .ouradata import get_oura_layout, get_oura_data

def register_layout(dash_app):
    """Creates the dashboard layout with the given dash_app."""
    dash_app.layout = html.Div(id='layout', children=
        [
            get_symptom_layout(),
            get_oura_layout(),
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
        return is_open, int(percent)

    @dash_app.callback(
        Output('heartrate', 'figure'), 
        Input('oura-sync-btn', 'n_clicks'), 
        Input('slider_average', 'value'),
    )
    def sync_oura_data(n_clicks, average):
        return get_oura_data(n_clicks, average)