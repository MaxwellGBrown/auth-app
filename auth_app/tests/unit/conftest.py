import pyramid.testing
import pytest

import auth_app.auth


@pytest.fixture
def test_config(request, ini_config):
    config = pyramid.testing.setUp()

    config.add_route('index', '/')
    config.add_route('home', '/home')

    authz_policy = auth_app.auth.authorization_policy()
    config.set_authorization_policy(authz_policy)
    # config.set_root_factory(RootFactory)

    settings = ini_config['app:main']
    auth_cfg = {k[5:]: v for k, v in settings.items() if k[:5] == "auth."}
    authn_policy = auth_app.auth.authentication_policy(
        callback=lambda: list(), **auth_cfg
    )
    config.set_authentication_policy(authn_policy)

    request.addfinalizer(pyramid.testing.tearDown)
    return config
