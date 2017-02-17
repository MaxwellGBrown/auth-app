from hashlib import sha1
import os

from pyramid.security import unauthenticated_userid
from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from auth_app.models.meta import Base, Session


def auth_callback(userid, request):
    """ AuthTxtAuthenticationPolicy(..., callback=auth_callback) """
    userid = unauthenticated_userid(request)
    if userid is None:
        return None

    user = Session.query(User).filter_by(user_id=userid).first()
    if user is not None:
        return user.permissions
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
    """ Authentication model w/ Authorization permissions """
    __tablename__ = "user"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(Unicode(256), unique=True, nullable=False)
    user_type = Column(Unicode(16), nullable=False, default="basic")

    # @property = .password
    _password = Column('password', Unicode(128), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": user_type,
        "polymorphic_identity": "basic"
    }

    # ACL Permissions associated w/ user_type="basic"
    permissions = tuple()

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


class AdminUser(User):
    """ Authentication model with administrator permissions """

    __mapper_args__ = {"polymorphic_identity": "admin"}

    permissions = ("admin")
