import pyramid.httpexceptions as http
import pytest

from auth_app.auth import User
from auth_app.forms import CreateUserForm


pytestmark = [
    pytest.mark.unit,
    pytest.mark.views,
    pytest.mark.admin,
]


def test_get_manage_user(test_config):
    """ UserManagementViews.manage_users returns users list """
    from auth_app.views.admin import UserManagementViews

    all_users = []  # TODO list a bunch of mock users

    request = test_config.DummyRequest()
    response = UserManagementViews(request).manage_users()

    assert "users" in response
    assert response["users"] == all_users


def test_get_manage_user_show_create_user_form(test_config):
    """ UserManagementViews.manage_users has the CreateUserForm """
    from auth_app.views.admin import UserManagementViews

    request = test_config.DummyRequest()
    response = UserManagementViews(request).manage_users()

    assert "create_user_form" in response
    assert isinstance(response["create_user_form"], CreateUserForm)
    assert len(response["create_user_form"].errors) == 0


def test_create_user_redirects(test_config, new_user_kwargs):
    """ UserManagementViews.create_user redirects """
    from auth_app.views.admin import UserManagementViews

    request = test_config.DummyRequest(params=new_user_kwargs)
    response = UserManagementViews(request).create_user()

    assert isinstance(response, http.HTTPFound)


def test_create_user_makes_user(test_config, new_user_kwargs):
    """ UserManagementViews.create_user inserts new user into DB """
    from auth_app.views.admin import UserManagementViews

    request = test_config.DummyRequest(post=new_user_kwargs)
    UserManagementViews(request).create_user()

    new_user = User  # TODO
    assert new_user.email == new_user_kwargs['email']
    assert new_user.user_type == new_user_kwargs['user_type']


@pytest.mark.parametrize("missing_kwargs", ["email"])
def test_create_user_required_arguments(test_config,
                                        new_user_kwargs, missing_kwargs):
    """ UserManagementViews.create_user fails when missing required values """
    from auth_app.views.admin import UserManagementViews

    new_user_kwargs.pop(missing_kwargs)

    request = test_config.DummyRequest(params=new_user_kwargs)
    response = UserManagementViews(request).create_user()

    assert len(response['create_user_form'].errors) > 0


def test_delete_user(test_user, test_config):
    """ UserManagementViews.delete_user removes user from DB """
    from auth_app.views.admin import UserManagementViews

    request = test_config.DummyRequest()
    request.context = User  # TODO

    UserManagementViews(request).delete_user()
    # TODO Raise an HTTP Exception


def test_delete_nonexistant_user(test_config):
    """ UserManagementViews.delete_user fails w/ nonexistant user """
    from auth_app.views.admin import UserManagementViews

    request = test_config.DummyRequest()
    request.context = None

    UserManagementViews(request).delete_user()
    # TODO Raise an HTTP Exception


@pytest.mark.skip(reason='Not Implemented')
def test_reset_user_sets_token(test_config, test_user):
    """ UserManagementViews.reset_user sets token """
    from auth_app.views.admin import UserManagementViews

    user = User  # TODO

    request = test_config.DummyRequest()
    request.context = user

    UserManagementViews(request).reset_user()

    assert user.token != test_user.token
    assert user.token is not None


@pytest.mark.skip(reason="Not Implemented")
def test_reset_user_changes_password(test_config, test_user):
    """ UserManagementViews.reset_user changes password """
    from auth_app.views.admin import UserManagementViews

    user = User  # TODO

    request = test_config.DummyRequest()
    request.context = user

    UserManagementViews(request).reset_user()

    assert user.validate(test_user._unhashed_password) is False


def test_reset_user_redirects_to_user_management(test_config, test_user):
    """ UserManagementViews.reset_user returns HTTPFound """
    from auth_app.views.admin import UserManagementViews

    user = User

    request = test_config.DummyRequest()
    request.context = user

    response = UserManagementViews(request).reset_user()
    assert isinstance(response, http.HTTPFound)
    assert response.location == request.route_url('manage_users')
