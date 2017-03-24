import pyramid.testing
import pytest
from webob.multidict import MultiDict

from auth_app.config import configure


@pytest.fixture
def test_config(request, ini_config):
    """ Create a testing Configurator to spawn DummyRequests """
    config = pyramid.testing.setUp()
    config.DummyRequest = DummyRequest  # request = config.DummyRequest(...)

    configure(config, **ini_config['app:main'])

    request.addfinalizer(pyramid.testing.tearDown)
    return config


class DummyRequest(pyramid.testing.DummyRequest):
    """ pyramid.testing.DummyRequest that turns params to MultiDict """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all these MultiDicts after initialization
        self.params = MultiDict(self.params)
        self.GET = MultiDict(self.GET)
        self.POST = MultiDict(self.POST)
