import configparser

import pytest

from auth_app.auth import User


def pytest_addoption(parser):
    parser.addoption(
      "--config", action="store", default="test.ini",
      help=".ini configuration used to initialize the application for testing"
    )


@pytest.fixture(scope="session")
def ini_filepath(request):
    """ returns argument specified by pytest --config=<ini_filepath> """
    return request.config.getoption("--config")


@pytest.fixture(scope="session")
def ini_config(ini_filepath):
    """ returns ConfigParser object created from ini_filepath """
    config = configparser.ConfigParser()
    config.read(ini_filepath)
    return config


@pytest.fixture
def new_user_kwargs():
    """
    **kwargs that model the values for a new User object.

    This is done so that a change to the user model doesn't require a change in
    every single test; just to this fixture!
    """
    # TODO
    return dict(
        email=User.email,
        password=User.password,
        user_type=User.user_type
    )


@pytest.fixture
def test_user():
    # TODO Actually make a test user
    return User


@pytest.fixture
def test_admin():
    # TODO Actually make a test admin
    return User
