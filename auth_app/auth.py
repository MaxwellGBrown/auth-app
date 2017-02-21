from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import unauthenticated_userid

from auth_app.models import Session, User


def authentication_policy(*args, **kwargs):
    return AuthTktAuthenticationPolicy(*args, **kwargs)


def authorization_policy(*args, **kwargs):
    return ACLAuthorizationPolicy(*args, **kwargs)


def auth_callback(userid, request):
    """ AuthTxtAuthenticationPolicy(..., callback=auth_callback) """
    userid = unauthenticated_userid(request)
    if userid is None:
        return None

    user = Session.query(User).filter_by(user_id=userid).first()
    if user is not None:
        return user.permissions
    else:
        return None
