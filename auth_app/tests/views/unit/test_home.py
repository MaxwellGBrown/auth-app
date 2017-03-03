import pyramid.testing
import pytest


pytestmark = [
    pytest.mark.unit
]


def test_home(test_config):
    """ home(request) returns {} """
    from auth_app.views.home import home

    request = pyramid.testing.DummyRequest()

    assert home(request) == {}
