from urllib.parse import urlparse

import pytest


pytestmark = [
    pytest.mark.functional,
    pytest.mark.usefixtures("rollback")
]


def test_get_login(test_app):
    """
    GET /login 200

    /login has a form w/ for user, password, and submit that POST to /login
    """
    response = test_app.get('/login', status=200)

    login_form = response.html.find(
        "form", attrs={"method": "POST"}
    )
    assert login_form
    assert urlparse(login_form['action']).path == '/login'

    assert login_form.find('input', attrs={'name': 'email'})
    assert login_form.find('input', attrs={'name': 'password'})
    assert login_form.find('input', attrs={'type': 'submit'})


def test_get_logout(test_app, as_test_user, ini_config):
    """ GET /logout while auth clears cookies & redirects to / """
    cookie_name = ini_config['app:main']['auth.cookie_name']

    response = test_app.get('/logout', status=302)

    # make sure the header was deleted!
    cookie = response.headers['Set-Cookie']
    assert cookie.split(" ")[0] == cookie_name + '=;'

    # assert you're being redirected to /
    location = urlparse(response.location)
    assert location.path == '/'

    redirect = response.follow()
    assert redirect.status == '200 OK'


def test_post_login(test_app, as_test_user, ini_config):
    """ POST /login authenticates & redirects to /home """
    cookie_name = ini_config['app:main']['auth.cookie_name']

    response = test_app.post(
        '/login',
        status=302,
        params={
            'email': as_test_user.email,
            'password': as_test_user._unhashed_password
        }
    )

    cookie = response.headers['Set-Cookie']
    assert cookie.split(" ")[0].startswith(cookie_name + '=')

    location = urlparse(response.location)
    assert location.path == '/home'

    redirect = response.follow()
    assert redirect.status == '200 OK'


def test_post_login_bad_password(test_app, test_user, ini_config):
    """ POST /login doesn't authenticate user w/ wrong password """
    response = test_app.post(
        '/login',
        status=200,
        params={
            'email': test_user.email,
            'password': 'WRONG PASSWORD'
        }
    )

    assert response.headers.get('Set-Cookie') is None


def test_post_login_bad_email(test_app, test_user):
    """ POST /login doesn't authenticate user w/ unregistered email """
    response = test_app.post(
        '/login',
        status=200,
        params={
            'email': 'bad@wrong.com',
            'password': test_user._unhashed_password
        }
    )

    assert response.headers.get('Set-Cookie') is None


def test_post_login_empty(test_app, test_user):
    """ POST /login handles empty form submission  """
    response = test_app.post('/login', status=200)

    assert response.headers.get('Set-Cookie') is None
