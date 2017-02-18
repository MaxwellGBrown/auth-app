import configparser

import alembic
from alembic.config import Config
import pytest
from sqlalchemy import engine_from_config, event
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
    user._unhashed_password = "password123"

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


@pytest.fixture(scope="session")
def test_admin(request, ini_config, alembic_head):
    """
    Returns a transient AdminUser object that represents an object in the db
    """
    engine = engine_from_config(
        configuration=ini_config['app:main'],
        prefix="sqlalchemy."
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    admin_user = app_model.AdminUser(
        email="admin@example.com",
        password="foobar12",
        user_type="admin"
    )
    admin_user._unhashed_password = "foobar12"

    session.add(admin_user)
    session.commit()

    session.refresh(admin_user)
    make_transient(admin_user)

    session.close()

    def remove_test_admin_user():
        session = Session()
        session.delete(admin_user)
        session.commit()

    return admin_user


@pytest.fixture(scope="function")
def rollback(request, ini_config):
    engine = engine_from_config(
        configuration=ini_config['app:main'],
        prefix="sqlalchemy."
    )

    connection = engine.connect()
    app_model.Base.metadata.bind = connection
    transaction = connection.begin()

    # start a SAVEPOINT
    app_model.Session.begin_nested()

    @event.listens_for(app_model.Session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    def revert_changes():
        app_model.Session.remove()
        transaction.rollback()
        connection.close()

    request.addfinalizer(revert_changes)
