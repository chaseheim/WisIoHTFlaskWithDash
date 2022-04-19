"""Flask config."""
from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

class Config:
    """Set Flask configuration variables from .env file."""

    # General Config
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    SQLALCHEMY_ECHO=environ.get("SQLALCHEMY_ECHO")

    # Cognito
    AWS_REGION = environ.get("AWS_REGION")
    AWS_COGNITO_DOMAIN = environ.get("AWS_COGNITO_DOMAIN")
    AWS_COGNITO_USER_POOL_ID = environ.get("AWS_COGNITO_USER_POOL_ID")
    AWS_COGNITO_USER_POOL_CLIENT_ID = environ.get("AWS_COGNITO_USER_POOL_CLIENT_ID")
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = environ.get("AWS_COGNITO_USER_POOL_CLIENT_SECRET")
    AWS_COGNITO_REDIRECT_URL = environ.get("AWS_COGNITO_REDIRECT_URL")
    AWS_COGNITO_LOGOUT_URL = environ.get("AWS_COGNITO_LOGOUT_URL")

    # Authlib client
    OURA_CLIENT_ID=environ.get("OURA_CLIENT_ID")
    OURA_CLIENT_SECRET=environ.get("OURA_CLIENT_SECRET")