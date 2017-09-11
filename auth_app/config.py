from pyramid.config import Configurator

import auth_app.auth
from auth_app.user import configure_cognito_idp
from auth_app.util import sub_settings


def configure(config, **settings):
    """ does initialization for main() so tests can also use config """

    config.include('pyramid_mako')

    # authorization
    authz_policy = auth_app.auth.authorization_policy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(auth_app.auth.root_factory)

    # authentication
    auth_cfg = sub_settings(settings, 'auth')
    authn_policy = auth_app.auth.authentication_policy(
        callback=auth_app.auth.auth_callback, **auth_cfg
    )
    config.set_authentication_policy(authn_policy)

    # aws cognito-idp to manage users & authentication
    aws_cfg = sub_settings(settings, 'aws')
    cognito_idp_cfg = sub_settings(settings, 'cognito_idp')
    configure_cognito_idp(region_name=aws_cfg['region_name'],
                          **cognito_idp_cfg)

    # request methods
    config.add_request_method(auth_app.auth.request_user, "user", reify=True)

    # standard routes
    config.add_route('index', '/')
    config.add_route('home', '/home')

    # auth routes
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('forgot_password', '/forgot_password')
    config.add_route('redeem', '/redeem/{token}',
                     factory=auth_app.auth.user_factory)

    # /admin/users
    config.add_route('manage_users', '/admin/users')
    config.add_route('create_user', '/admin/users/create')
    config.add_route('reset_user', '/admin/users/reset/{user_id}',
                     factory=auth_app.auth.user_factory)
    config.add_route('delete_user', '/admin/users/delete/{user_id}',
                     factory=auth_app.auth.user_factory)


def main(global_config, **settings):
    config = Configurator(settings=settings)
    configure(config, **settings)
    config.scan()
    return config.make_wsgi_app()
