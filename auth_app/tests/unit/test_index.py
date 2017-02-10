import pyramid.testing
import pytest


@pytest.mark.unit
def test_index(test_config):
    from auth_app.views import index

    request = pyramid.testing.DummyRequest()

    assert index(request) == {}
