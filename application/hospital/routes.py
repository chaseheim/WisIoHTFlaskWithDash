from flask import (
    Blueprint,
    redirect,
    session,
    g,
    url_for,
    request
)
from flask_cognito_lib.decorators import auth_required

bp = Blueprint('hospital_bp', __name__)

@bp.before_app_request
def load_access_in_session():
    # TODO: Change to retrieve auth from db
    g.hospital = False
    if session.get('is_authed_hospital') != None:
        g.hospital = True

# Location to being authorization process
@bp.route('/hospital/authorize', methods=['GET', 'POST'])
@auth_required()
def authorize_hospital():
    # User ID is the user id of the hospital user

    # TODO: Check if user is already authorized, if not continue, else error
    # TODO: Check that userid is valid, check that it is a hospital user
    # TODO: Store authorization in db for reuse at login
    
    if request.method == 'POST':
        hospital = request.form.get('hospitalSelection')
        session['is_authed_hospital'] = hospital
    
    return redirect(url_for('settings'))

# Location to unauthorize with a previously authorized hospital
@bp.route('/hospital/unauthorize', methods=['GET', 'POST'])
@auth_required()
def unauthorize_hospital():
    # User ID is the user id of the hospital user

    # TODO: Check if user is already authorized, if so continue and get authed id
    # TODO: Remove authorization in db for reuse at login
    
    session.pop('is_authed_hospital', None)
    return redirect(url_for('settings'))