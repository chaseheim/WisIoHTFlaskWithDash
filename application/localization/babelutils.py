from application import babel
from flask import session

@babel.localeselector
def get_locale():
    """Return the desired langurage from the session setting"""
    
    if session.get('localization_preference') != None:
        return session.get('localization_preference')

    return None