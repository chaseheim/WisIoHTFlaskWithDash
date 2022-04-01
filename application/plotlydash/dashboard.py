import dash
from dash import dcc
from dash import html
from flask_cognito_lib.decorators import auth_required

# TODO: pick up here
def is_authed():
    @auth_required()
    def check():
        return "imsotired"

    if check() == "imsotired":
        return True
    return False
    

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/style.css',
        ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div([
        html.H1(children="Testing123"),
        html.Div()
        ])

    return dash_app.server