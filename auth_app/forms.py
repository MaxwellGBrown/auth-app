import wtforms
import wtforms.fields as fields
import wtforms.validators as val


class CreateUserForm(wtforms.Form):
    """ A Form for creating a new user"""

    email = fields.StringField(
        label="Email",
        validators=[val.DataRequired(), val.Email()]
    )

    user_type = fields.SelectField(
        label="User Type",
        choices=[("basic", "Basic"), ("admin", "Admin")],
        default="basic"
    )


class LoginForm(wtforms.Form):
    """ A Form for authorization """

    email = fields.StringField("Email", validators=[val.DataRequired()])
    password = fields.PasswordField(
        "Password",
        validators=[val.DataRequired()]
    )
