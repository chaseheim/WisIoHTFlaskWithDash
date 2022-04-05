from flask import(
    Blueprint,
    current_app,
    jsonify,
    url_for
)
from authlib.integrations.flask_client import OAuth

bp = Blueprint('oura_bp', __name__)

# Initialize OAuthlib
oauth = OAuth(current_app)

# Compliance fix for accessing protected data
def oura_api_header(session):
    def _fix(url, headers, data):
        headers['Host'] = 'api.ouraring.com'
        return url, headers, data
    session.register_compliance_hook('protected_request', _fix)

# Initialize OAuth client
oura = oauth.register(
    name='oura',
    authorize_url='https://cloud.ouraring.com/oauth/authorize',
    access_token_url='https://api.ouraring.com/oauth/token',
    api_base_url='https://cloud.ouraring.com/v2/usercollection/',
    compliance_fix=oura_api_header,
    client_kwargs={
        'token_endpoint_auth_method': 'client_secret_post',
        'token_placement': 'header'
    }
)

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
    # Save token somewhere - db

    # Testing getting some data
    resp = oura.get('personal_info', token=token)
    data = resp.json()
    return jsonify(data)