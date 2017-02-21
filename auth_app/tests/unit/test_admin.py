import pyramid.httpexceptions as http
import pyramid.testing
import pytest

from auth_app.models import User


pytestmark = pytest.mark.usefixtures("rollback")


@pytest.mark.unit
def test_get_manage_user(test_config, alembic_head):
    """ UserManagementViews.manage_users returns users list """
    from auth_app.views.admin import UserManagementViews

    all_users = User.all()

    request = pyramid.testing.DummyRequest()
    response = UserManagementViews(request).manage_users()

    assert "users" in response
    assert response["users"] == all_users


@pytest.mark.unit
def test_create_user_redirects(test_config, alembic_head, new_user_kwargs):
    """ UserManagementViews.create_user redirects """
    from auth_app.views.admin import UserManagementViews

    request = pyramid.testing.DummyRequest(params=new_user_kwargs)
    response = UserManagementViews(request).create_user()

    assert isinstance(response, http.HTTPFound)


@pytest.mark.unit
def test_create_user_makes_user(test_config, alembic_head, new_user_kwargs):
    """ UserManagementViews.create_user inserts new user into DB """
    from auth_app.views.admin import UserManagementViews

    # just make sure the new_user isn't already in the DB
    results = User.all(email=new_user_kwargs['email'])
    assert len(results) == 0

    request = pyramid.testing.DummyRequest(params=new_user_kwargs)
    UserManagementViews(request).create_user()

    new_user = User.one(email=new_user_kwargs['email'])
    assert new_user.email == new_user_kwargs['email']
    assert new_user.user_type == new_user_kwargs['user_type']


@pytest.mark.unit
def test_create_user_email_unique(test_config, alembic_head, new_user_kwargs,
                                  test_user):
    """ UserManagementViews.create_user fails w/ non-unique email address """
    from auth_app.views.admin import UserManagementViews

    new_user_kwargs['email'] = test_user.email

    count = len(User.all())

    request = pyramid.testing.DummyRequest(params=new_user_kwargs)
    UserManagementViews(request).create_user()

    assert len(User.all()) == count


@pytest.mark.unit
@pytest.mark.parametrize("missing_kwargs", ["email", "password"])
def test_create_user_required_arguments(test_config, alembic_head,
                                        new_user_kwargs, missing_kwargs):
    """ UserManagementViews.create_user fails when missing required values """
    from auth_app.views.admin import UserManagementViews

    count = len(User.all())

    new_user_kwargs.pop(missing_kwargs)

    request = pyramid.testing.DummyRequest(params=new_user_kwargs)
    UserManagementViews(request).create_user()

    assert len(User.all()) == count
