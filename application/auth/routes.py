from flask import (
    Blueprint, 
    redirect, 
    url_for, 
    jsonify, 
    session, 
    g
)
from flask_cognito_lib.decorators import (
    cognito_login,
    cognito_login_callback,
    cognito_logout
)
from flask_cognito_lib.exceptions import (
    CognitoGroupRequiredError, 
    AuthorisationRequiredError
)

bp = Blueprint('auth_bp', __name__)

@bp.before_app_request
def load_logged_in_user():
    """Get user info and store in g. Runs before app request."""
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
    return  redirect(url_for('home'))

@bp.errorhandler(CognitoGroupRequiredError)
def missing_group_error_handler(err):
    # Register an error handler if the user hits an "@auth_required" route
    # but is not in all of groups specified
    return jsonify("Group membership does not allow access to this resource"), 403

@bp.errorhandler(AuthorisationRequiredError)
def auth_error_handler(err):
    # Register an error handler if the user hits an "@auth_required" route
    # but is not logged in to redirect them to the Cognito UI
    return redirect(url_for("login")), 403