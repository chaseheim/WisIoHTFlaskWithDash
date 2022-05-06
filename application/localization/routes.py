from flask import (
    Blueprint,
    redirect,
    session,
    url_for,
    request
)
from flask_cognito_lib.decorators import auth_required

bp = Blueprint('localization_bp', __name__)

@bp.route('/lang', methods=['GET', 'POST'])
@auth_required()
def set_localization():
    # TODO: Set localization preference in session
    
    if request.method == 'POST':
        preference = request.form.get('localizationPreference')
        if preference != None:
            session.pop('localization_preference')
            session['localization_preference'] = preference
    
    return redirect(url_for('settings'))