# Compliance fix for accessing protected data
def oura_api_header(session):
    '''Compliance fix for OAuth2 with Oura. Requires additional data in header.'''
    def _fix(url, headers, data):
        # Oura required Host: api.ouraring.com in the header for API access
        headers['Host'] = 'api.ouraring.com'
        return url, headers, data
    session.register_compliance_hook('protected_request', _fix)

def register_provider(app):
    '''Initialize OAuth provider: oura'''
    # Get OAuthlib from flask app
    oauth = app.extensions.get('authlib.integrations.flask_client')
    oauth.register(
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
