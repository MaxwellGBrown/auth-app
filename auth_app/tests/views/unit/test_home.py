import pytest


pytestmark = [
    pytest.mark.unit,
    pytest.mark.views
]


def test_home(test_config):
    """ home(request) returns {} """
    from auth_app.views.home import home

    request = test_config.DummyRequest()

    assert home(request) == {}
