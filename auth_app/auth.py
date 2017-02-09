from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def authentication_policy(*args, **kwargs):
    return AuthTktAuthenticationPolicy(*args, **kwargs)


def authorization_policy(*args, **kwargs):
    return ACLAuthorizationPolicy(*args, **kwargs)
