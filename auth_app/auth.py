from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import pyramid.security as security

from auth_app.models import Session, User


class RootFactory(object):
    __acl__ = [
        (security.Allow, security.Authenticated, 'authenticated'),
        (security.Allow, 'admin', 'admin')
    ]

    def __init__(self, request):
        self.request = request


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
