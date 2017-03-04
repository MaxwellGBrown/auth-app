import pytest
import sqlalchemy.orm.exc as orm_exc

from auth_app.models import User


pytestmark = [
    pytest.mark.functional,
    pytest.mark.views,
    pytest.mark.usefixtures("rollback")
]


def test_get_manage_users(test_app, as_test_admin):
    """ GET /admin/users 200 shows all users while auth as an admin """
    response = test_app.get('/admin/users', status=200)

    all_users = User.all()

    for user in all_users:
        assert user.email in response


def test_get_manage_users_unauthenticated(test_app):
    """ GET /admin/users 403 while unauthenticated """
    test_app.get('/admin/users', status=403)


def test_get_manage_users_unauthorized(test_app, as_test_user):
    """ GET /admin/users 403 without authorization """
    test_app.get('/admin/users', status=403)


def test_post_create_user(test_app, as_test_admin, new_user_kwargs):
    """ POST /admin/users creates new user """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=302)

    new_user = User.one(email=new_user_kwargs['email'])
    assert new_user
    assert new_user.user_type == new_user_kwargs['user_type']
    assert new_user.token is not None


def test_post_create_user_unauthorized(test_app, as_test_user,
                                       new_user_kwargs):
    """ POST /admin/users 403's without authorization """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=403)


def test_post_create_user_unauthenticated(test_app, new_user_kwargs):
    """ POST /admin/users 403's without authorization """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=403)


def test_get_delete_user(test_app, as_test_admin, test_user):
    """ GET /admin/users/delete/<id> removes associated user """
    response = test_app.get(
        '/admin/users/delete/{}'.format(test_user.user_id), status=302
    )

    with pytest.raises(orm_exc.NoResultFound):
        User.one(user_id=test_user.user_id)

    redirect = response.follow()
    assert redirect.status == '200 OK'

    assert test_user.email not in redirect.html.find(id="user-table")


def test_post_delete_user_unauthenticated(test_app, test_user):
    """ POST /admin/users/delete/<id> 403's without authentication """
    test_app.post(
        '/admin/users/delete/{}'.format(test_user.user_id), status=403
    )


def test_get_delete_user_unauthorized(test_app, as_test_user, test_admin):
    """ POST /admin/users/delete/<id> 403's without authorization """
    test_app.post(
        '/admin/users/delete/{}'.format(test_admin.user_id), status=403
    )


def test_get_delete_user_nonexistant(test_app, as_test_admin):
    """ POST /admin/users/delete/<id> 404's if user doesn't exist """

    test_app.post('/admin/users/delete/9999', status=404)
