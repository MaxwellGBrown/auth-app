import pytest

import auth_app.forms as forms


pytestmark = [
    pytest.mark.unit,
    pytest.mark.forms,
]


@pytest.mark.parametrize('email_value,is_valid', [
    ('justastring', False),
    ('nodomain@', False),
    ('nouser.com', False),
    ('user@domain.com', True),
])
def test_create_user_form_valid_email(new_user_kwargs, email_value, is_valid):
    """
    CreateUserForm.email must be a valid email address

    Currently just using wtforms.validators.email, so not "perfect" but good
    """
    message = "Invalid email address."
    new_user_kwargs['email'] = email_value
    create_user_form = forms.CreateUserForm(data=new_user_kwargs)
    create_user_form.validate()
    invalid_email = message in create_user_form.email.errors
    assert invalid_email != is_valid


@pytest.mark.parametrize('user_type_value,is_valid', [
    ('admin', True),
    ('basic', True),
    ('not_a_user_type', False),
    ('', False)
])
def test_create_user_form_valid_user_type(new_user_kwargs, user_type_value,
                                          is_valid):
    """ CreateUserForm.user_type requires one of the preset options """
    new_user_kwargs['user_type'] = user_type_value
    create_user_form = forms.CreateUserForm(data=new_user_kwargs)
    create_user_form.validate()
    invalid_choice = "Not a valid choice" in create_user_form.user_type.errors
    assert invalid_choice != is_valid
