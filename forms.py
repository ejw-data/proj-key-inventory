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
    email = StringField("Input your Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


def userform_instance(form_request=None):
    user_form = CreateUserForm(form_request)

    title_results = Titles.query.order_by(Titles.title_id.desc()).all()
    title_query_list = [(i.title_id, i.title.title()) for i in title_results]
    title_options = title_query_list
    user_form.title.choices = title_options

    role_results = Roles.query.order_by(Roles.role_id.desc()).all()
    role_query_list = [(i.role_id, i.user_role.title()) for i in role_results]
    user_form.role.choices = role_query_list

    return user_form


class CreateBuildingForm(FlaskForm):
    """
    Building Form fields
    """


class CreateRoomForm(FlaskForm):
    """
    Room Form fields
    """
