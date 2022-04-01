from flask import Blueprint, redirect, url_for, jsonify
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
    """Logout the user and delete the JSON Web Token cookie."""
    return redirect(url_for('home'))

@bp.route('/postlogout')
def postlogout():
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
    return redirect(url_for("login"))