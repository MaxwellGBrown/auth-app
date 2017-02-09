import pyramid.testing
import pytest


@pytest.fixture
def test_config(request):
    config = pyramid.testing.setUp()

    request.addfinalizer(pyramid.testing.tearDown)
    return config
