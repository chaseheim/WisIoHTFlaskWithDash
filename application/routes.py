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

test_dict = {
        '24e6bb30-2b3e-4ca1-89c3-11666ad20f00': {
            'given_name': 'Alfred',
            'family_name': 'Robinson',
            'birthdate': '2000-01-01',
            'email': 'example@example.com',
            'phone_number': '+11111111111',
            'probability': 0,
        },
        '24e6bb30-2b3e-4ca1-89c3-11666ad20f01': {
            'given_name': 'John',
            'family_name': 'Doe',
            'birthdate': '2000-01-02',
            'email': 'doejohn@example.com',
            'phone_number': '+11111111112',
            'probability': 35,
        },
        '24e6bb30-2b3e-4ca1-89c3-11666ad20f02': {
            'given_name': 'Alice',
            'family_name': 'Doe',
            'birthdate': '2000-01-03',
            'email': 'doealice@example.com',
            'phone_number': '+11111111113',
            'probability': 60,
        },
        '24e6bb30-2b3e-4ca1-89c3-11666ad20f03': {
            'given_name': 'Bob',
            'family_name': 'Doe',
            'birthdate': '2000-01-04',
            'email': 'doebob@example.com',
            'phone_number': '+11111111114',
            'probability': 86,
        },
        '24e6bb30-2b3e-4ca1-89c3-11666ad20f04': {
            'given_name': 'Edward',
            'family_name': 'Snowden',
            'birthdate': '2000-01-05',
            'email': 'snowden.edward@protonmail.com',
            'phone_number': '+11111111115',
            'probability': 0,
        },
    }

@app.route('/hospitaldash')
@auth_required(groups=['hospital'])
def hospitaldash():
    """Dashboard for hospital staff to interact with patient data."""
    # TODO: Make SQL query for usernames that are linked with hospital username
    # TODO: Organize into dict

    hospital_user = session.get('claims').get('username')

    return render_template('hospitaldash.html', users=test_dict)

@app.route('/hospitaldash/<userid>')
@auth_required(groups=['hospital'])
def inspectuser(userid):
    # TODO: Query specific user, check if hospital user is allowed to access user
    return render_template('inspectuser.html', user=test_dict.get(userid), userid=userid)


@app.errorhandler(CognitoGroupRequiredError)
def missing_group_error_handler(err):
    # Register an error handler if the user hits an "@auth_required" route
    # but is not in all of groups specified

    # TODO: Change to actual unauthed page jsonify wont work outside debug
    return jsonify("Group membership does not allow access to this resource")

@app.errorhandler(AuthorisationRequiredError)
def auth_error_handler(err):
    # Register an error handler if the user hits an "@auth_required" route
    # but is not logged in to redirect them to the Cognito UI
    # TODO: Add a specific page for this error with link to the login page
    return redirect(url_for("auth_bp.login"))