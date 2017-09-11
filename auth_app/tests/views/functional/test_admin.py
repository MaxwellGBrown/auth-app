import pytest

from auth_app.auth import User


pytestmark = [
    pytest.mark.functional,
    pytest.mark.views,
    pytest.mark.admin,
]


def test_get_manage_users(test_app, as_test_admin):
    """ GET /admin/users 200 shows all users while auth as an admin """
    response = test_app.get('/admin/users', status=200)

    all_users = {}  # TODO list users here

    user_table = response.html.find(id="user-table")
    assert user_table

    for row in user_table.select('tbody > tr'):
        user_cell = row.select('td:nth-of-type(1)')[0]
        user_id = int(user_cell.text.strip())
        user = all_users[user_id]

        # so I can just do <str> in row
        row = str(row)

        assert user.email in row
        if user.token:
            assert user.token in row
        assert '/admin/users/delete/{}'.format(user_id) in row
        assert '/admin/users/reset/{}'.format(user_id) in row


def test_get_manage_users_shows_create_user_form(test_app, as_test_admin):
    """ GET /admin/users 200 shows the create user form """
    response = test_app.get('/admin/users', status=200)

    create_user_form = response.html.find(id="create-user-form")
    assert create_user_form
    assert create_user_form.get('method') == 'POST'
    assert create_user_form.get('action').endswith('/admin/users/create')

    email_input = create_user_form.find(attrs={"name": "email"})
    assert email_input

    user_type_select = create_user_form.find(attrs={"name": "user_type"})
    assert user_type_select

    submit_input = create_user_form.find(attrs={"type": "submit"})
    assert submit_input


def test_get_manage_users_unauthenticated(test_app):
    """ GET /admin/users 403 while unauthenticated """
    test_app.get('/admin/users', status=403)


@pytest.mark.skip('default is to be admin when authenticated for now')
def test_get_manage_users_unauthorized(test_app, as_test_user):
    """ GET /admin/users 403 without authorization """
    test_app.get('/admin/users', status=403)


@pytest.mark.skip(reason="Should we have fxnal tests that call Cognito?")
def test_post_create_user(test_app, as_test_admin, new_user_kwargs):
    """ POST /admin/users creates new user """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=302)

    new_user = User  # TODO Update when User model is implemented
    assert new_user
    assert new_user.user_type == new_user_kwargs['user_type']
    assert new_user.token is not None


@pytest.mark.parametrize('missing_field', ['email'])
def test_post_create_user_requires_fields(test_app, as_test_admin,
                                          new_user_kwargs, missing_field):
    """ POST /admin/users shows error feedback """
    new_user_kwargs.pop(missing_field)
    response = test_app.post('/admin/users/create', params=new_user_kwargs)

    create_user_form = response.html.find(id="create-user-form")

    # unit tests can check which fields do/don't have errors
    # fxnal tests are just going to check that there WAS an error
    errors = create_user_form.find(class_='errors')
    assert errors


@pytest.mark.skip('For now all authenticated is admin')
def test_post_create_user_unauthorized(test_app, as_test_user,
                                       new_user_kwargs):
    """ POST /admin/users 403's without authorization """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=403)


def test_post_create_user_unauthenticated(test_app, new_user_kwargs):
    """ POST /admin/users 403's without authorization """
    test_app.post('/admin/users/create', params=new_user_kwargs, status=403)


@pytest.mark.skip(reason="Should we have fxnal tests that call Cognito?")
def test_get_delete_user(test_app, as_test_admin, test_user):
    """ GET /admin/users/delete/<id> removes associated user """
    response = test_app.get(
        '/admin/users/delete/{}'.format(test_user.user_id), status=302
    )

    # TODO Implement a fake deletion

    redirect = response.follow()
    assert redirect.status == '200 OK'

    assert test_user.email not in redirect.html.find(id="user-table")


@pytest.mark.skip(reason="501 Not Implemented")
def test_post_delete_user_unauthenticated(test_app, test_user):
    """ POST /admin/users/delete/<id> 403's without authentication """
    test_app.post(
        '/admin/users/delete/{}'.format(test_user.user_id), status=403
    )


@pytest.mark.skip(reason="501 Not Implemented")
def test_get_delete_user_unauthorized(test_app, as_test_user, test_admin):
    """ POST /admin/users/delete/<id> 403's without authorization """
    test_app.post(
        '/admin/users/delete/{}'.format(test_admin.user_id), status=403
    )


@pytest.mark.skip(reason="501 Not Implemented")
def test_get_delete_user_nonexistant(test_app, as_test_admin):
    """ POST /admin/users/delete/<id> 404's if user doesn't exist """

    test_app.post('/admin/users/delete/9999', status=404)


@pytest.mark.skip(reason="Should we fxnal tests that call Cognito?")
def test_reset_user(test_app, as_test_admin, test_user):
    """
    GET /admin/users/reset/<id> resets associated users password & sets token
    """
    user = User  # TODO

    response = test_app.get('/admin/users/reset/{}'.format(test_user.user_id))
    assert response.location.endswith('/admin/users')

    assert user.token != test_user.token
    assert user.token is not None
    assert user.validate(test_user._unhashed_password) is False


@pytest.mark.skip(reason="501 Not Implemented")
def test_reset_nonexistant_user(test_app, as_test_admin):
    """ GET /admin/users/reset/<id> 404's on nonexistant user """

    test_app.get('/admin/users/reset/999', status=404)


@pytest.mark.skip(reason="501 Not Implemented")
def test_reset_user_unauthenticated(test_app, test_user):
    """ GET /admin/users/reset/<id> 403's while unauthenticated """

    user = User  # TODO

    test_app.get(
        '/admin/users/reset/{}'.format(test_user.user_id), status=403
    )

    assert user.token == test_user.token
    assert user.validate(test_user._unhashed_password) is True


@pytest.mark.skip(reason="501 Not Implemented")
def test_reset_user_unauthorized(test_app, test_admin, as_test_user):
    """ GET /admin/users/reset/<id> 403's if unauthorized """

    user = User  # TODO

    test_app.get(
        '/admin/users/reset/{}'.format(test_admin.user_id), status=403
    )

    assert user.token == test_admin.token
    assert user.validate(test_admin._unhashed_password) is True
