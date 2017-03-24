import pytest


pytestmark = [
    pytest.mark.unit,
    pytest.mark.views
]


def test_index(test_config):
    """ index(request) == {} """
    from auth_app.views.index import index

    request = test_config.DummyRequest()

    assert index(request) == {}
