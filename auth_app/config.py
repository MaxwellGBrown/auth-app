from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import auth_app.auth
import auth_app.models as app_model
from auth_app.request import request_user


def configure(config, **settings):
    """ does initialization for main() so tests can also use config """

    config.include('pyramid_mako')

    # authorization
    authz_policy = auth_app.auth.authorization_policy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(auth_app.auth.root_factory)

    # authentication
    auth_cfg = {k[5:]: v for k, v in settings.items() if k[:5] == "auth."}
    authn_policy = auth_app.auth.authentication_policy(
        callback=auth_app.auth.auth_callback, **auth_cfg
    )
    config.set_authentication_policy(authn_policy)

    # request methods
    config.add_request_method(request_user, "user", reify=True)

    # standard routes
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('home', '/home')

    # /admin/users
    config.add_route('manage_users', '/admin/users')
    config.add_route('create_user', '/admin/users/create')
    config.add_route('delete_user', '/admin/users/delete/{user_id}',
                     factory=app_model.User.route_factory)


def main(global_config, **settings):
    config = Configurator(settings=settings)

    # connect ORM model to database
    engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
    app_model.bind_engine(engine)

    configure(config, **settings)

    config.scan()

    return config.make_wsgi_app()
