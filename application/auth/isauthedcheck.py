from functools import wraps

from flask import request

from flask_cognito_lib.decorators import cfg
from flask_cognito_lib.decorators import cognito_auth
from flask_cognito_lib.exceptions import (
    AuthorisationRequiredError,
    TokenVerifyError,
)


def auth_required(fn):
    """An altered decorator to protect a route with AWS Cognito
    See flask_cognito_lib.decorators.auth_required for original function.
    """

    @wraps(fn)
    def decorator(*args, **kwargs):

        # Try and validate the access token stored in the cookie
        try:
            access_token = request.cookies.get(cfg.COOKIE_NAME)
            cognito_auth.verify_access_token(
                token=access_token,
                leeway=cfg.cognito_expiration_leeway,
            )
            valid = True

        except (TokenVerifyError, KeyError):
            valid = False

        if valid:
            return fn(*args, **kwargs)

        raise AuthorisationRequiredError

    return decorator