from flask import (
    Blueprint, 
    redirect, 
    url_for, 
    session, 
    g
)
from flask_cognito_lib.decorators import (
    cognito_login,
    cognito_login_callback,
    cognito_logout
)

bp = Blueprint('auth_bp', __name__)

@bp.before_app_request
def load_logged_in_user():
    """Get user info and store in g. Runs before view request."""
    user_info = session.get('user_info')

    if user_info is None:
        g.user = None
    else:
        g.user = user_info

@bp.route('/login', methods=['GET', 'POST'])
@cognito_login
def login():
    """Redirect to the Cognito Hosted UI for login / registration."""
    pass

@bp.route('/postlogin', methods=['GET'])
@cognito_login_callback
def postlogin():
    """After a successful login, store the access token as a cookie and redirect."""
    # TODO: Check if account has authorized with oura and add indicator to session: session['is_authed_oura'] = True
    # TODO: Check if account has authorized with a hospital account and add indicator to session: session['is_authed_hospital'] = userid (userid being the hospital account)
    return redirect(url_for('home'))

@bp.route('/logout', methods=['GET', 'POST'])
@cognito_logout
def logout():
    """Logout the user from the Cognito User Pool."""
    # No logic is required here as it simply redirects to Cognito.
    pass

@bp.route('/postlogout')
def postlogout():
    """Cognito redirect here, redirect back to home."""
    # Clear left over user session
    session.clear()
    # TODO: Create logged out confirmation page
    return  redirect(url_for('home'))