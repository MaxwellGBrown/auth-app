import sqlalchemy.orm.exc as orm_exc
import wtforms
import wtforms.fields as fields
import wtforms.validators as val

from auth_app.models import User


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

    def validate_email(form, field):
        """
        Raised ValidationError if value is alredy exists in db as User.email
        """
        try:
            User.one(email=field.data)
            raise val.ValidationError(
                'Email "{}" is already in use!'.format(field.data)
            )
        except orm_exc.NoResultFound:
            pass


class LoginForm(wtforms.Form):
    """ A Form for authorization """

    email = fields.StringField("email", validators=[val.DataRequired()])
    password = fields.PasswordField(
        "password",
        validators=[val.DataRequired()]
    )

    @property
    def user(form):
        """ Retrieve user associated w/ data stored in form.email """
        try:
            return getattr(form, '_user')
        except AttributeError:
            pass

        try:
            form._user = User.one(email=form.email.data)
        except orm_exc.NoResultFound:
            form._user = None

        return form._user

    def validate_email(form, field):
        """ Checks that a user w/ email exists """
        if form.user is None:
            raise val.StopValidation("No account associated with this email")

    def validate_password(form, field):
        """ Checks that a User.validate(`password`) returns True """
        if form.user is None:
            # We can't validate the password w/o a User
            return

        if not form.user.validate(field.data):
            raise val.ValidationError("Incorrect password")
