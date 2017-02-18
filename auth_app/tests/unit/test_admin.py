import pyramid.testing
import pytest

from auth_app.models import User


@pytest.mark.unit
def test_get_manage_user(test_config, alembic_head):
    """ UserManagementViews.manage_users returns users list """
    from auth_app.views.admin import UserManagementViews

    all_users = User.all()

    request = pyramid.testing.DummyRequest()
    response = UserManagementViews(request).manage_users()

    assert "users" in response
    assert response["users"] == all_users
