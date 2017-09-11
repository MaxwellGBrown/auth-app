import pyramid.httpexceptions as http
import pytest

from auth_app.auth import User


pytestmark = [
    pytest.mark.unit,
    pytest.mark.views,
]


def test_get_login(test_config):
    """ AuthViews.get_login returns {} """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest()

    response = AuthViews(request).get_login()
    assert 'login_form' in response


def test_logout(test_config, ini_config):
    """ AuthViews.logout clears the authz cookie & redirects to index """
    from auth_app.views.auth import AuthViews

    cookie_name = ini_config['app:main']['auth.cookie_name']

    request = test_config.DummyRequest(
        cookies=[(cookie_name, 'DELETE_ME')]
    )

    response = AuthViews(request).logout()
    assert isinstance(response, http.HTTPFound)
    assert response.headers['Location'].endswith('/')
    assert response.headers['Set-Cookie'].startswith(cookie_name + "=;")


def test_post_login(test_config, test_user, ini_config):
    """ AuthViews.post_login success redirects to index w/ cookies """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest(
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


@pytest.mark.skip("No check for bad passwords")
def test_post_login_bad_password(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorization w/ bad password """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest(
        post={
            "email": test_user.email,
            "password": "BAD PASSWORD"
        }
    )

    response = AuthViews(request).post_login()
    assert 'login_form' in response
    assert response['login_form'].errors


def test_post_login_no_password(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorization w/ no password """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest(
        post={
            "email": test_user.email
        }
    )

    response = AuthViews(request).post_login()
    assert 'login_form' in response
    assert response['login_form'].errors


def test_post_login_no_email(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorization w/ no email """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest(
        post={
            "password": "anything"
        }
    )

    response = AuthViews(request).post_login()
    assert 'login_form' in response
    assert response['login_form'].errors


@pytest.mark.skip("No check for bad passwords")
def test_post_login_bad_email(test_config, test_user, ini_config):
    """ LoginView.post_login fails authorizationw w/ bad email """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest(
        post={
            "email": "bad@fail.com",
            "password": test_user._unhashed_password
        }
    )

    response = AuthViews(request).post_login()
    assert 'login_form' in response
    assert response['login_form'].errors


def test_post_login_no_credentials(test_config, ini_config):
    """ LoginView.post_login fails authorization w/ no credentials """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest()

    response = AuthViews(request).post_login()
    assert 'login_form' in response
    assert response['login_form'].errors


def test_get_redeem_token(test_config, test_user):
    """ RedeemTokenView.get_redeem_token works w/ valid User.token """
    from auth_app.views.auth import RedeemTokenViews

    request = test_config.DummyRequest()
    request.context = test_user

    RedeemTokenViews(request).get_redeem_token()


def test_post_redeem_token_redirects_to_login(test_config, test_user,
                                              new_user_kwargs):
    """ RedeemTokenView.post_redeem_token clears token """
    from auth_app.views.auth import RedeemTokenViews

    user = User  # TODO

    post = {k: v for k, v in new_user_kwargs.items() if k == "password"}
    request = test_config.DummyRequest(post=post)
    request.context = user

    response = RedeemTokenViews(request).post_redeem_token()
    assert isinstance(response, http.HTTPFound)
    assert response.location == request.route_url('login')


def test_forgot_password_nonexistant_user_returns_dict(test_config):
    """ AuthViews.forgot_password handles bad email """
    from auth_app.views.auth import AuthViews

    request = test_config.DummyRequest(post={"email": "not@real"})

    response = AuthViews(request).forgot_password()

    assert 'login_form' in response
