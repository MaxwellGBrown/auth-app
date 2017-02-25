from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import pyramid.security as security

from auth_app.models import Session, User, AppBase


def root_factory(request):
    return AppBase


def authentication_policy(*args, **kwargs):
    return AuthTktAuthenticationPolicy(*args, **kwargs)


def authorization_policy(*args, **kwargs):
    return ACLAuthorizationPolicy(*args, **kwargs)


def auth_callback(userid, request):
    """ AuthTxtAuthenticationPolicy(..., callback=auth_callback) """
    userid = security.unauthenticated_userid(request)
    if userid is None:
        return None

    user = Session.query(User).filter_by(user_id=userid).first()
    if user is not None:
        return user.permissions
    else:
        return None
