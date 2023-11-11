from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    ValidationError,
    BooleanField,
    SelectField,
)
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length
from models import db, Roles, Titles


# Create Form Class
class LoginForm(FlaskForm):
    """
    Login Form fields
    """

    username = StringField("Input your Username", validators=[DataRequired()])
    password = StringField("Input your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateUserForm(FlaskForm):
    """
    User Form fields
    """

    first_name = StringField("Input your First Name", validators=[DataRequired()])
    last_name = StringField("Input your Last Name", validators=[DataRequired()])
    title = SelectField("Select Title", coerce=int, validators=[InputRequired()])
    role = SelectField("Select Role", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Submit")


def userform_instance(form_request=None):
    user_form = CreateUserForm(form_request)

    title_list = [(1, "Option 1"), (2, "Option 2")]
    user_form.title.choices = title_list

    role_list = [(1, "General user"), (2, "Admin")]
    user_form.role.choices = role_list

    return user_form
class CreateBuildingForm(FlaskForm):
    """
    Building Form fields
    """


class CreateRoomForm(FlaskForm):
    """
    Room Form fields
    """
