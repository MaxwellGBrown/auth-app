import pytest

import auth_app.forms as forms

pytestmark = [
    pytest.mark.unit,
    pytest.mark.forms,
    # these forms have a validator that relies on the `user` table; needs bind
    pytest.mark.usefixtures('alembic_head'),
    pytest.mark.usefixtures('rollback')
]


def test_login_form_validates_good_credentials(test_user):
    """ LoginForm.validate() succeeds w/ good credentials """
    login_form = forms.LoginForm(email=test_user.email,
                                 password=test_user._unhashed_password)
    assert login_form.validate() is True


def test_login_form_nonexistant_email_fails_validation():
    """
    LoginForm.validate() fails validation with a bad email
    """
    login_form = forms.LoginForm(email="bad@nonexistant.com",
                                 password="irrelevant")
    assert login_form.validate() is False


def test_login_form_nonexistant_email_shows_error():
    """
    LoginForm.validate() shows errors for email & not password
    """
    login_form = forms.LoginForm(email="bad@nonexistant.com",
                                 password="irrelevant")
    login_form.validate()
    assert "No account associated with this email" in login_form.email.errors
    assert not login_form.password.errors


def test_login_form_bad_password_fails_validation(test_user):
    """
    LoginForm.validate() fails with a bad password
    """
    login_form = forms.LoginForm(obj=test_user, password="irrelevant")
    assert login_form.validate() is False


def test_login_form_bad_password_shows_error(test_user):
    """
    LoginForm.validate() shows password errors and NOT email errors
    """
    login_form = forms.LoginForm(obj=test_user, password="irrelevant")
    login_form.validate()
    assert "Incorrect password" in login_form.password.errors
    assert not login_form.email.errors


def test_login_form_email_required():
    """ LoginForm.validate() fails w/o email """
    login_form = forms.LoginForm(password="irrelevant")
    assert login_form.validate() is False
    assert "This field is required." in login_form.email.errors


def test_login_form_password_required(test_user):
    """ LoginForm.validate() fails w/o password """
    login_form = forms.LoginForm(email=test_user.email)
    assert login_form.validate() is False
    assert "This field is required." in login_form.password.errors
