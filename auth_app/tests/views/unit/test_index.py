import pyramid.testing
import pytest


pytestmark = [
    pytest.mark.unit,
    pytest.mark.views
]


def test_index(test_config):
    """ index(request) == {} """
    from auth_app.views.index import index

    request = pyramid.testing.DummyRequest()

    assert index(request) == {}
