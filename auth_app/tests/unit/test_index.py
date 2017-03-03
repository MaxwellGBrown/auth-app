import pyramid.testing
import pytest


pytestmark = [
    pytest.mark.unit
]


def test_index(test_config):
    """ index(request) == {} """
    from auth_app.views.index import index

    request = pyramid.testing.DummyRequest()

    assert index(request) == {}
