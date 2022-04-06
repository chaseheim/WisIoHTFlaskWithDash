"""Routes for parent Flask app."""
from flask import (
    jsonify, 
    redirect, 
    render_template, 
    url_for, 
    session,
    current_app as app
)
from flask_cognito_lib.decorators import auth_required
from flask_cognito_lib.exceptions import (
    CognitoGroupRequiredError, 
    AuthorisationRequiredError
)

@app.route('/')
def home():
    """Landing page."""
    return render_template('index.html')

@app.route("/health")
def health():
    """Return a JSON response containing status OK. Used for automatic health checks.
    Returns
    -------
    flask.Response
        200 OK response
    """
    return jsonify({'status': 'ok'}), 200

@app.route('/admin')
@auth_required(groups=['admin'])
def admin():
    # Will error if there is no session
    # Okay since you can't access this page without being logged in
    return jsonify(session)

@app.route('/settings')
@auth_required()
def settings():
    """Landing page."""
    return render_template('settings.html')

@app.errorhandler(CognitoGroupRequiredError)
def missing_group_error_handler(err):
    # Register an error handler if the user hits an "@auth_required" route
    # but is not in all of groups specified
    return jsonify("Group membership does not allow access to this resource")

@app.errorhandler(AuthorisationRequiredError)
def auth_error_handler(err):
    # Register an error handler if the user hits an "@auth_required" route
    # but is not logged in to redirect them to the Cognito UI
    # TODO: Add a specific page for this error with link to the login page
    return redirect(url_for("auth_bp.login"))