import configparser

import pytest


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
