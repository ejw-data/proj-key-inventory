from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField, SelectField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length


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


class CreateBuildingForm(FlaskForm):
    """
    Building Form fields
    """


class CreateRoomForm(FlaskForm):
    """
    Room Form fields
    """
