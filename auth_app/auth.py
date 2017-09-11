import boto3
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import pyramid.httpexceptions as http
import pyramid.security as security


class AppBase(object):
    __acl__ = (
        (security.Allow, security.Authenticated, 'authenticated'),
        (security.Allow, 'admin', 'admin')
    )


def root_factory(request):
    return AppBase


def user_factory(request):
    """
    Match a user to request such that request.context = user

    `user_id` is in request.matchdict to query the user by.
    """
    raise http.HTTPNotImplemented()


def authentication_policy(*args, **kwargs):
    return AuthTktAuthenticationPolicy(*args, **kwargs)


def authorization_policy(*args, **kwargs):
    return ACLAuthorizationPolicy(*args, **kwargs)


def auth_callback(userid, request):
    """ AuthTxtAuthenticationPolicy(..., callback=auth_callback) """
    userid = security.unauthenticated_userid(request)
    if userid is None:
        return None

    # TODO: Return a user's ACLs'
    return ("admin",)


class RequestCognitoIdp(object):
    """
    A configured object that returns an Cognito sesion on call

    >>> config.add_request_method(RequestCognitoIdp(**config), "idp")
    """

    def __init__(self, region_name):
        self.region_name = region_name

    def __call__(self, request):
        session = boto3.session.Session(region_name=self.region_name)
        return session.client('cognito-identiy')


class UserManager(object):
    """
    An interface for working w/ user classes.

    Why?
    Because the views don't care what the objects look like, they just want
    objects they can work with.

    So, if you're (I don't know...) switching from an ORM Auth model to an
    authentication service then you'd have to change how each view interfaces
    with the User model object (e.g. querying the database vs requesting from
    the Identity Provider) instead of just dropping in a new class that just
    interfaces with the provider instead of the database (but still returns
    similar objects).
    """

    def list_users(self, offset=0):
        """ Return a list of users """
        return []  # TODO


def request_user(request):
    """ config.add_request_method(request_user, "user", reify=True) """
    user_id = security.unauthenticated_userid(request)  # noqa

    # TODO: Return user object to attach to request.user
    return User


class User(object):
    """ Placeholder class for a User resource """
    user_id = 1

    email = 'max@amberengine.com'
    password = 'this_is_the_password'
    _unhashed_password = 'this_is_the_password'

    user_type = 'admin'

    token = 'TOKEN'

    @classmethod
    def validate(cls, password):
        return password == 'this_is_the_password'
