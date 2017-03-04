from hashlib import sha1
import os

from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from auth_app.models.meta import Base


class User(Base):
    """ Authentication model for all Users """
    __tablename__ = "user"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(Unicode(256), unique=True, nullable=False)
    user_type = Column(Unicode(16), nullable=False, default="basic")

    token = Column(Unicode(32), unique=True, nullable=True, default=None)
    # @property = .password
    _password = Column('password', Unicode(128), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": user_type,
        "polymorphic_identity": None
    }

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

    def set_token(self):
        """ Sets a randomized User.token """
        self.token = sha1(os.urandom(40)).hexdigest()

    def reset(self):
        """ Rehashes password as a random string and sets a token """
        self.set_token()
        self.password = sha1(os.urandom(40)).hexdigest()


class BasicUser(User):
    """ Authentication model w/ Authorization permissions """

    __mapper_args__ = {"polymorphic_identity": "basic"}

    permissions = tuple()


class AdminUser(User):
    """ Authentication model with administrator permissions """

    __mapper_args__ = {"polymorphic_identity": "admin"}

    permissions = ("admin",)
