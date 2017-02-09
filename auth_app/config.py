from pyramid.config import Configurator
import pyramid.security as security
from sqlalchemy import engine_from_config

from auth_app.models import request_user, auth_callback
import auth_app.models as app_model
import auth_app.auth


class RootFactory(object):
    __acl__ = [
        (security.Allow, security.Authenticated, 'authenticated')
    ]

    def __init__(self, request):
        self.request = request


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    # database
    engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
    app_model.bind_engine(engine, create_all=True)

    # authentication
    auth_cfg = {k[5:]: v for k, v in settings.items() if k[:5] == "auth."}
    authn_policy = auth_app.auth.authentication_policy(
        callback=auth_callback, **auth_cfg
    )
    config.set_authentication_policy(authn_policy)

    # authorization
    authz_policy = auth_app.auth.authorization_policy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(RootFactory)

    # request methods
    config.add_request_method(request_user, "user", reify=True)

    # routes
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('home', '/home')

    config.scan()

    return config.make_wsgi_app()
