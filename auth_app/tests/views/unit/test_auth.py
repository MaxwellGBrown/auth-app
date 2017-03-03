import pyramid.httpexceptions as http
import pyramid.testing
import pytest


pytestmark = [
    pytest.mark.unit,
    pytest.mark.views,
    pytest.mark.usefixtures("rollback")
]


def test_get_login(test_config):
    """ AuthViews.get_login returns {} """
    from auth_app.views.auth import AuthViews

    request = pyramid.testing.DummyRequest()

    assert AuthViews(request).get_login() == {}


def test_logout(test_config, ini_config):
    """ AuthViews.logout clears the authz cookie & redirects to index """
    from auth_app.views.auth import AuthViews

    cookie_name = ini_config['app:main']['auth.cookie_name']

    request = pyramid.testing.DummyRequest(
        cookies=[(cookie_name, 'DELETE_ME')]
    )

    response = AuthViews(request).logout()
    assert isinstance(response, http.HTTPFound)
    assert response.headers['Location'].endswith('/')
    assert response.headers['Set-Cookie'].startswith(cookie_name + "=;")


def test_post_login(test_config, test_user, ini_config):
    """ AuthViews.post_login success redirects to index w/ cookies """
    from auth_app.views.auth import AuthViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": test_user.email,
            "password": test_user._unhashed_password
        }
    )

    response = AuthViews(request).post_login()
    assert isinstance(response, http.HTTPFound)
    assert response.headers['Location'].endswith('/home')
    cookie_name = ini_config['app:main']['auth.cookie_name']
    assert response.headers['Set-Cookie'].startswith(cookie_name)


def test_post_login_bad_password(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorization w/ bad password """
    from auth_app.views.auth import AuthViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": test_user.email,
            "password": "BAD PASSWORD"
        }
    )

    response = AuthViews(request).post_login()
    assert response == {}


def test_post_login_no_password(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorization w/ no password """
    from auth_app.views.auth import AuthViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": test_user.email
        }
    )

    response = AuthViews(request).post_login()
    assert response == {}


def test_post_login_no_email(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorization w/ no email """
    from auth_app.views.auth import AuthViews

    request = pyramid.testing.DummyRequest(
        post={
            "password": "anything"
        }
    )

    response = AuthViews(request).post_login()
    assert response == {}


def test_post_login_bad_email(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorizationw w/ bad email """
    from auth_app.views.auth import AuthViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": "bad@fail.com",
            "password": test_user._unhashed_password
        }
    )

    response = AuthViews(request).post_login()
    assert response == {}


def test_post_login_no_credentials(test_config, ini_config):
    """ LoginView.post_login fails authorization w/ no credentials """
    from auth_app.views.auth import AuthViews

    request = pyramid.testing.DummyRequest()

    response = AuthViews(request).post_login()
    assert response == {}
