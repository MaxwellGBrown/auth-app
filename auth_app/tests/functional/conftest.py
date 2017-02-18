from six.moves import http_cookiejar
import pytest

import auth_app.auth
from auth_app.config import main
from auth_app.models.user import auth_callback


@pytest.fixture(scope="class")
def test_app(request, ini_config, ini_filepath, alembic_head):
    """ returns pyramid app object initialized as a webtest.TestApp object """
    from webtest import TestApp

    global_config = {
        "__file__": ini_filepath,  # config file used to initialize app
        "here": "auth_app"  # filepath of the app
    }

    settings = ini_config["app:main"]

    app = main(global_config, **settings)
    return TestApp(app)


@pytest.fixture(scope="function")
def as_test_user(request, test_app, test_user, ini_config):
    auth_cfg = {
        k[5:]: v for k, v in ini_config['app:main'].items()
        if k.startswith('auth.')
    }

    authn_policy = auth_app.auth.authentication_policy(
        callback=auth_callback, **auth_cfg
    )

    environ = {  # required by auth_policy's CookieHelper
        "REMOTE_ADDR": "0.0.0.0",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "9999"
    }

    http_request = test_app.app.request_factory(environ)
    headers = authn_policy.remember(http_request, test_user.user_id)

    # cookie_name=<cookie>!userid_type:int; ...other_cookies
    auth_cookie = headers[0][1].split(' ')[0]
    cookie_name, cookie = auth_cookie.split('=')

    # WebTest.TestApp.set_cookie double quotes cookie values
    # test_app.set_cookie(cookie_name, cookie)
    test_app.cookiejar.set_cookie(
        http_cookiejar.Cookie(
            name=cookie_name,
            value=cookie,
            # "required positional args"
            version=0,
            port=None,
            port_specified=False,
            domain=".localhost",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
        )
    )

    request.addfinalizer(test_app.reset)
    return test_user


@pytest.fixture(scope="function")
def as_test_admin(request, test_app, test_admin, ini_config):
    auth_cfg = {
        k[5:]: v for k, v in ini_config['app:main'].items()
        if k.startswith('auth.')
    }

    authn_policy = auth_app.auth.authentication_policy(
        callback=auth_callback, **auth_cfg
    )

    environ = {  # required by auth_policy's CookieHelper
        "REMOTE_ADDR": "0.0.0.0",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "9999"
    }

    http_request = test_app.app.request_factory(environ)
    headers = authn_policy.remember(http_request, test_admin.user_id)

    # cookie_name=<cookie>!userid_type:int; ...other_cookies
    auth_cookie = headers[0][1].split(' ')[0]
    cookie_name, cookie = auth_cookie.split('=')

    # WebTest.TestApp.set_cookie double quotes cookie values
    # test_app.set_cookie(cookie_name, cookie)
    test_app.cookiejar.set_cookie(
        http_cookiejar.Cookie(
            name=cookie_name,
            value=cookie,
            # "required positional args"
            version=0,
            port=None,
            port_specified=False,
            domain=".localhost",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
        )
    )

    request.addfinalizer(test_app.reset)
    return test_admin
