from .meta import Base, Session, AppBase  # noqa
from .user import User, AdminUser  # noqa


def bind_engine(engine, create_all=False):
    """ binds engine to Session & Base.metadata """
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    if create_all is True:
        Base.metadata.create_all(engine)
