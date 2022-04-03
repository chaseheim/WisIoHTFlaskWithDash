import dash
from application.plotlydash.dashboard_layout import (
    dashboard_layout
)

# External dash stylesheets
external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3',
        'crossorigin': 'anonymous'
    }
]

# External dash JavaScript
external_scripts = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p',
        'crossorigin': 'anonymous'
    }
]

def init_dashboard(server):
    """Initialize the Plotly Dash dashboard."""
    # __name__ needed for asset folder detection
    dash_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/dashboard/',
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts
    )

    # Call function from dashboard_layout.py to configure the appearance of the dashboard
    dashboard_layout(dash_app)

    return dash_app.server