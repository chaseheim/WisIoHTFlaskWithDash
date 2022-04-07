"""Initializes the Flask app."""
from flask import Flask
from flask_cors import CORS
from flask_cognito_lib import CognitoAuth
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

# Create extension objects
middleware = CORS() #  CORS middleware
cognito = CognitoAuth() # Cognito auth for use with AWS Cognito Hosted UI
db = SQLAlchemy() # SQLAlchemy for database management
oauth = OAuth() # OAuthLib for OAuth2 management

def create_app() -> Flask:
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize extensions
    middleware.init_app(app)
    cognito.init_app(app)
    db.init_app(app)
    oauth.init_app(app)

    # Register OAuthlib provider
    from .oauthlib.provider import register_provider
    register_provider()

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