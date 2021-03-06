import pytest


pytestmark = [
   pytest.mark.functional,
   pytest.mark.views
]


def test_get_home(test_app, as_test_user):
    """ GET /home 200 if authenticated """
    response = test_app.get('/home', status=200)
    assert response


def test_get_home_403(test_app):
    """ GET /home 403 if unauthenticated """
    response = test_app.get('/home', status=403)
    assert response
