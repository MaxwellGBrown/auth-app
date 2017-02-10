import configparser

import alembic
from alembic.config import Config
import pytest
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import make_transient

import auth_app.models as app_model


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


@pytest.fixture(scope="session")
def test_user(request, ini_config, alembic_head):
    """ Returns a transient User object that represents an object in the db """
    engine = engine_from_config(
        configuration=ini_config['app:main'],
        prefix="sqlalchemy."
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    user = app_model.User(
        email="test@example.com",
        password="password123"
    )

    session.add(user)
    session.commit()

    session.refresh(user)
    make_transient(user)

    session.close()

    def remove_test_user():
        session = Session()
        session.delete(user)
        session.commit()

    return user
