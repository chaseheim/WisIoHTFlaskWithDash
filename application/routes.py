"""Routes for parent Flask app."""
from flask import jsonify, render_template, session
from flask import current_app as app
from flask_cognito_lib.decorators import auth_required

@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.html',
        title='Plotly Dash Flask Application',
        description='Embed Plotly Dash into a Flask application.',
        template='home-template',
        body="This is a homepage served with Flask."
    )

@app.route("/health")
def health():
    """Return a JSON response containing status OK. Used for automatic health checks
    Returns
    -------
    flask.Response
        200 OK response
    """
    return jsonify({'status': 'ok'})

@app.route('/claims')
@auth_required(groups=['admin'])
def claims():
    # Will error if there is no session
    # Okay since you can't access this page without being logged in
    return jsonify(session)

@app.route('/admin')
@auth_required(groups=['admin'])
def admin():
    # Will error if there is no session
    # Okay since you can't access this page without being logged in
    return jsonify(session['claims']['cognito:groups'])