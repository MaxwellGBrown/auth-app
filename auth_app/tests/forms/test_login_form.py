import pytest

import auth_app.forms as forms

pytestmark = [
    pytest.mark.unit,
    pytest.mark.forms,
]


def test_login_form_validates_good_credentials(test_user):
    """ LoginForm.validate() succeeds w/ good credentials """
    login_form = forms.LoginForm(email=test_user.email,
                                 password=test_user._unhashed_password)
    assert login_form.validate() is True


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
