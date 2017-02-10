from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Session = scoped_session(sessionmaker())


class AppBase(object):
    """ A declarative base mixin that lets you run queries as cls methods """

    @classmethod
    def query(cls, **kwargs):
        return Session.query(cls).filter_by(**kwargs)

    @classmethod
    def one(cls, **kwargs):
        return cls.query(**kwargs).one()

    @classmethod
    def all(cls, **kwargs):
        return cls.query(**kwargs).all()


Base = declarative_base(cls=AppBase)
