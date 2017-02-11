import pyramid.testing
import pytest


@pytest.mark.unit
def test_home(test_config):
    from auth_app.views import home

    request = pyramid.testing.DummyRequest()

    assert home(request) == {}
