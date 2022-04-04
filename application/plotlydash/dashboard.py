import pathlib
import dash
from flask import render_template_string
from ..auth.isauthedcheck import auth_required
from application.plotlydash.dashboard_layout import (
    register_layout,
    init_callbacks
)

# Method to protect dash views/routes
def protect_dashviews(server):
    for view_func in server.view_functions:
        if view_func.startswith('/dashboard/'):
            server.view_functions[view_func] = auth_required(server.view_functions[view_func])

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

    # Register Jinja2 template
    with server.test_request_context():
        layout_dash = pathlib.Path(pathlib.Path(__file__).parent.parent.joinpath("templates").joinpath("dashboard.html"))
        
        with open(layout_dash, "r") as f:
            html_body = render_template_string(f.read())
        
        comments_to_replace = ("metas", "favicon", "css", "app_entry", "config", "scripts", "renderer")
        for comment in comments_to_replace:
            html_body = html_body.replace(f"<!-- {comment} -->", "{%" + comment + "%}")
        
        dash_app.index_string = html_body

    # Configure appearance of the dashboard
    register_layout(dash_app)

    # Register callbacks
    init_callbacks(dash_app)

    # Protect dashapp views
    protect_dashviews(server)
    
    return dash_app.server