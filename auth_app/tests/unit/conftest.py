import pyramid.testing
import pytest

from auth_app.config import configure


@pytest.fixture
def test_config(request, ini_config):
    config = pyramid.testing.setUp()

    configure(config, **ini_config['app:main'])

    request.addfinalizer(pyramid.testing.tearDown)
    return config
