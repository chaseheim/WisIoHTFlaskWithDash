"""Initializes the Flask app."""
from flask import Flask
from flask_cors import CORS
from flask_cognito_lib import CognitoAuth
from authlib.integrations.flask_client import OAuth

def init_app() -> Flask:
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize CORS middleware
    CORS(app)

    # Initialize Cognito auth
    CognitoAuth(app)

    # Initialize OAuthlib
    OAuth(app)
    # Register OAuthlib provider
    from .oauthlib.provider import register_provider
    register_provider(app)

    with app.app_context():
        # Include main routes
        from . import routes

        # Register Blueprints
        from .auth import routes as auth_routes
        app.register_blueprint(auth_routes.bp)
        from .oauthlib import routes as oauthlib_routes
        app.register_blueprint(oauthlib_routes.bp)

        # Import Dash application
        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app) # Register isolated Dash app into parent Flask app

        return app