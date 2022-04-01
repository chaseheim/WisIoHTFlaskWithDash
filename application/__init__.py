"""Initializes the Flask app."""
from flask import Flask
from flask_cognito_lib import CognitoAuth
from flask_cors import CORS

def init_app() -> Flask:
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize CORS middleware
    CORS(app)

    # Initialize Cognito auth
    CognitoAuth(app)

    with app.app_context():
        # Include our Routes
        from . import routes
        from .auth import routes as auth_routes

        # Register Blueprints
        app.register_blueprint(auth_routes.bp)

        # Import Dash application
        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app) # Register isolated Dash app into parent Flash app

        return app