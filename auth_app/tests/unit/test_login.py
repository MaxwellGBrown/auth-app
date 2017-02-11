import pyramid.httpexceptions as http
import pyramid.testing
import pytest


@pytest.mark.unit
def test_get_login(test_config):
    from auth_app.views import LoginViews

    request = pyramid.testing.DummyRequest()

    assert LoginViews(request).get_login() == {}


@pytest.mark.unit
def test_logout(test_config, ini_config):
    from auth_app.views import LoginViews

    cookie_name = ini_config['app:main']['auth.cookie_name']

    request = pyramid.testing.DummyRequest(
        cookies=[(cookie_name, 'DELETE_ME')]
    )

    response = LoginViews(request).logout()
    assert isinstance(response, http.HTTPFound)
    assert response.headers['Location'].endswith('/')
    assert response.headers['Set-Cookie'].startswith(cookie_name + "=;")


@pytest.mark.unit
def test_post_login(test_config, test_user, ini_config, rollback):
    from auth_app.views import LoginViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": test_user.email,
            "password": test_user._unhashed_password
        }
    )

    response = LoginViews(request).post_login()
    assert isinstance(response, http.HTTPFound)
    assert response.headers['Location'].endswith('/home')
    cookie_name = ini_config['app:main']['auth.cookie_name']
    assert response.headers['Set-Cookie'].startswith(cookie_name)


@pytest.mark.unit
def test_post_login_bad_password(test_config, test_user, ini_config, rollback):
    from auth_app.views import LoginViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": test_user.email,
            "password": "BAD PASSWORD"
        }
    )

    response = LoginViews(request).post_login()
    assert response == {}


@pytest.mark.unit
def test_post_login_no_password(test_config, test_user, ini_config, rollback):
    from auth_app.views import LoginViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": test_user.email
        }
    )

    response = LoginViews(request).post_login()
    assert response == {}


@pytest.mark.unit
def test_post_login_no_email(test_config, test_user, ini_config, rollback):
    from auth_app.views import LoginViews

    request = pyramid.testing.DummyRequest(
        post={
            "password": "anything"
        }
    )

    response = LoginViews(request).post_login()
    assert response == {}


@pytest.mark.unit
def test_post_login_bad_email(test_config, test_user, ini_config, rollback):
    from auth_app.views import LoginViews

    request = pyramid.testing.DummyRequest(
        post={
            "email": "bad@fail.com",
            "password": test_user._unhashed_password
        }
    )

    response = LoginViews(request).post_login()
    assert response == {}


@pytest.mark.unit
def test_post_login_no_credentials(test_config, ini_config, rollback):
    from auth_app.views import LoginViews

    request = pyramid.testing.DummyRequest()

    response = LoginViews(request).post_login()
    assert response == {}
