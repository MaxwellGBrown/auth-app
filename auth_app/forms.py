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
