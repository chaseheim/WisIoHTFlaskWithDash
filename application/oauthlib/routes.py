from requests.exceptions import HTTPError
from flask import(
    Blueprint,
    current_app,
    redirect,
    session,
    g,
    url_for
)
from application import oauth

bp = Blueprint('oura_bp', __name__)
#oura = current_app.extensions.get('authlib.integrations.flask_client').create_client('oura')
oura = oauth.create_client('oura')

@bp.before_app_request
def load_token_in_session():
    # Change to retrieve token from db
    g.token = False
    g.token_failed = False
    if session.get('is_authed_oura') is True:
        g.token = True
    if session.get('is_authed_oura_failed') is True:
        g.token_failed = True
        session.pop('is_authed_oura_failed', None)

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

    # Verify token validity - max 5 tries
    for n in range(5):
        try:
            # Get the personal_info scope from Oura
            response = oura.get('personal_info', token=token)
            response.raise_for_status()
            profile = response.json()

            # If a previous attempt failed, clear it from session
            if session.get('is_authed_oura_failed') is True:
                session.pop('is_authed_oura_failed')
            # Indicate in session that use is authorized with Oura
            session['is_authed_oura'] = True

            # TODO: Save token and profile somewhere - db and add an indicator to session (not the token itself)
            print(profile)

            break
        except HTTPError as exc:
            code = exc.response.status_code
            session['is_authed_oura_failed'] = True
            # TODO: Remove on deploy
            print('ERROR CODE ON ACCESS: ' + str(code))
            # 401 will occur if the user failed to select the personal_info scope
            if code in [401]:
                continue
        raise

    return redirect('settings')

@bp.route('/unauthorize')
def unauthorize_oura():
    session.pop('is_authed_oura', None)
    session.pop('is_authed_oura_failed', None)
    return redirect('settings')
    