import configparser

import alembic
from alembic.config import Config
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


@pytest.fixture(scope="session")
def alembic_head(request, ini_filepath):
    alembic_cfg = Config(ini_filepath)
    alembic.command.upgrade(alembic_cfg, "head")

    def alembic_base():
        alembic.command.downgrade(alembic_cfg, "base")

    request.addfinalizer(alembic_base)
