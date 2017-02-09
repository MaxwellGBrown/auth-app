from hashlib import sha1
import os

from pyramid.security import unauthenticated_userid

from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.hybrid import hybrid_property
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


def bind_engine(engine, create_all=False):
    """ binds engine to Session & Base.metadata """
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    if create_all is True:
        Base.metadata.create_all(engine)


def auth_callback(userid, request):
    """ AuthTxtAuthenticationPolicy(..., callback=auth_callback) """
    userid = unauthenticated_userid(request)
    if userid is None:
        return None

    user = Session.query(User).filter_by(user_id=userid).first()
    if user is not None:
        # return user principals a list of strings
        return []
    else:
        return None


def request_user(request):
    """ config.add_request_method(request_user, "user", reify=True) """
    user_id = unauthenticated_userid(request)
    if user_id is not None:
        user = Session.query(User).filter_by(user_id=user_id).first()
        return user
    else:
        return None


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(Unicode(256), unique=True)
    _password = Column('password', Unicode(128))  # @property = .password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, password):
        # password arg is assumed UTF-8
        salt = sha1(os.urandom(40))
        salted_pwd = password + salt.hexdigest()
        sha1_hash = sha1(salted_pwd.encode("UTF-8"))
        self._password = salt.hexdigest() + sha1_hash.hexdigest()

    def validate(self, password):
        """ Returns True if `password` matches unhashed User._password """
        combined_password = password + self.password[:40]
        hashed_password = sha1(combined_password.encode("UTF-8"))
        passwords_match = self.password[40:] == hashed_password.hexdigest()
        return passwords_match
