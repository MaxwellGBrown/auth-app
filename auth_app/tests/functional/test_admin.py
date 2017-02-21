import pytest

from auth_app.models import User


pytestmark = pytest.mark.usefixtures("rollback")


@pytest.mark.functional
def test_get_manage_users(test_app, as_test_admin):
    """ GET /admin/users 200 shows all users while auth as an admin """
    response = test_app.get('/admin/users', status=200)

    all_users = User.all()

    for user in all_users:
        assert user.email in response


@pytest.mark.functional
def test_get_manage_users_unauthenticated(test_app):
    """ GET /admin/users 403 while unauthenticated """
    test_app.get('/admin/users', status=403)


@pytest.mark.functional
def test_get_manage_users_unauthorized(test_app, as_test_user):
    """ GET /admin/users 403 without authorization """
    test_app.get('/admin/users', status=403)


@pytest.mark.functional
def test_post_create_user(test_app, as_test_admin, new_user_kwargs):
    """ POST /admin/users creates new user """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=302)

    new_user = User.one(email=new_user_kwargs['email'])
    assert new_user
    assert new_user.validate(new_user_kwargs['password'])
    assert new_user.user_type == new_user_kwargs['user_type']


@pytest.mark.functional
def test_post_create_user_unauthorized(test_app, as_test_user,
                                       new_user_kwargs):
    """ POST /admin/users 403's without authorization """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=403)
