from flask import(
    Blueprint,
    current_app,
    redirect,
    session,
    g,
    url_for
)

bp = Blueprint('oura_bp', __name__)
oura = current_app.extensions.get('authlib.integrations.flask_client').create_client('oura')

@bp.before_app_request
def load_token():
    # Change to retrieve token from db
    g.token = False
    if not session.get('is_authed_oura') is None:
        g.token = True

# Location to begin authorization process
@bp.route('/oura')
def login_oura():
    redirect_uri = url_for('oura_bp.authorize_oura', _external=True)
    return oura.authorize_redirect(redirect_uri)

# Redirect URL for recieving OAuth2 code
@bp.route('/authorize')
def authorize_oura():
    token = oura.authorize_access_token()
    print('Token recieved: ' + str(token))

    # Verify token validity
    resp = oura.get('personal_info', token=token)
    resp.raise_for_status()
    profile = resp.json()

    # TODO: Save token and profile somewhere - db and add an indicator to session (not the token itself)
    session['is_authed_oura'] = True

    return redirect('settings')

@bp.route('/unauthorize')
def unauthorize_oura():
    session.pop('is_authed_oura', None)
    return redirect('settings')
    