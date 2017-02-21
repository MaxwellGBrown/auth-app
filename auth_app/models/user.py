from hashlib import sha1
import os

from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from auth_app.models.meta import Base


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

    permissions = ("admin",)
