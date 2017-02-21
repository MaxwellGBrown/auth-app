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

    @classmethod
    def route_factory(cls, request):
        """
        Standardized cls request_method for route's URL Dispatch factory.

        >>> config.add_route(factory=cls.route_factory)

        Using this method, the ORM object that corresponds to the URL can be
        provided to a view via request.context, instead of a view running the
        query itself. This makes unit tests much easier to write & maintain!

        For more complex traversals, either override this method or define a
        new factory class.
        """
        return cls.one(**request.matchdict)


Base = declarative_base(cls=AppBase)
