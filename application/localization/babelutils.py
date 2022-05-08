from application import babel
from flask import session

@babel.localeselector
def get_locale():
    """Return the desired langurage from the session setting"""

    match session.get('localization_preference'):
        case 'es':
            return 'es'
        case 'zh':
            return 'zh'
    
    # If all else fails, return English
    return 'en'