import pytest

from auth_app.models.user import User, BasicUser, AdminUser
from auth_app.models.meta import Session


pytestmark = [
    pytest.mark.unit,
    pytest.mark.models,
    pytest.mark.usefixtures("rollback")
]


def test_admin_user_has_admin_permission(test_admin):
    """ User with user_type="admin" has "admin" in .permissions """
    admin_user = User.one(user_id=test_admin.user_id)
    assert "admin" in admin_user.permissions


def test_basic_user_does_not_have_admin_permission(test_user):
    """ User with user_type="basic" DOES NOT have "admin" in .permissions """
    basic_user = User.one(user_id=test_user.user_id)
    assert "admin" not in basic_user.permissions


def test_polymorphic_mapping_user_to_basic_user(test_user):
    """ Queries to User in ORM map to BasicUser """
    user = User.one(user_id=test_user.user_id)
    assert isinstance(user, BasicUser)


def test_polymorphic_mapping_user_to_admin_user(test_admin):
    """ Queries to User in ORM map to BasicUser """
    user = User.one(user_id=test_admin.user_id)
    assert isinstance(user, AdminUser)


def test_polymorphic_mapping_fails_with_bad_usertype(new_user_kwargs):
    """ Cannot creat new user w/ non-mapped .user_type """
    new_user_kwargs["user_type"] = "BAD"
    user = User(**new_user_kwargs)
    Session.add(user)
    Session.commit()


def test_set_password_hashes_users_password(test_user):
    """ User.set_password hashes User._password """
    previous_password = test_user.password
    test_user.password = "hello world"
    assert test_user.password != "hello world"
    assert test_user.password != previous_password


def test_user_validate_password_success(test_user):
    """
    User.validate returns True if unhashed password matches hashed password
    """
    test_user.password = "hello_world"
    assert test_user.validate("hello_world") is True


def test_user_validate_password_failure(test_user):
    """
    User.validate returns False if unhashed password doesn't match hashed pass
    """
    assert test_user.validate("BAD PASSWORD") is False


def test_user_reset_changes_token(test_user):
    """ User.reset() changes the users token """
    user = User.one(user_id=test_user.user_id)
    user.reset()
    Session.add(user)
    Session.commit()
    Session.refresh(user)
    assert user.token != test_user.token
    assert user.token is not None


def test_user_reset_changes_password(test_user):
    """ User.reset changes the users password """
    user = User.one(user_id=test_user.user_id)
    user.reset()
    Session.add(user)
    Session.commit()
    Session.refresh(user)
    assert user.validate(test_user._unhashed_password) is False


def test_user_set_token_changes_token(test_user):
    """ User.set_token() randomizes changes the users token """
    user = User.one(user_id=test_user.user_id)
    user.set_token()
    assert user.token != test_user.token
    assert user.token is not None
    Session.commit()
