from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from auth_app.models import request_user, auth_callback
import auth_app.models as app_model


def main(global_config, **settings):
    config = Configurator(settings=settings)

    # database
    engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
    app_model.bind_engine(engine, create_all=True)

    # authentication
    auth_cfg = {k[5:]: v for k, v in settings.items() if k[:5] == "auth."}
    authn_policy = AuthTktAuthenticationPolicy(
        callback=auth_callback, **auth_cfg
    )
    config.set_authentication_policy(authn_policy)

    # authorization
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    # config.set_root_factory(RootFactory)

    # request methods
    config.add_request_method(request_user, "user", reify=True)

    # routes
    config.add_route('index', '/')

    config.scan()

    return config.make_wsgi_app()
