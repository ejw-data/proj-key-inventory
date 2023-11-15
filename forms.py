from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    PasswordField,
    ValidationError,
    BooleanField,
    SelectField,
    EmailField,
)
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length
from models import Roles, Titles, RoomClassification, Buildings, Rooms, Approvers


# Create Form Class
class LoginForm(FlaskForm):
    """
    Login Form fields
    """

    username = EmailField("Input your Username", validators=[DataRequired()])
    password = PasswordField("Input your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    """
    Registration Form fields
    """

    username = EmailField("Input your Username", validators=[DataRequired()])
    password = PasswordField(
        "Input your Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must match"),
        ],
    )
    password2 = PasswordField("Retype your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateUserForm(FlaskForm):
    """
    User Form fields
    """

    first_name = StringField("Input your First Name", validators=[DataRequired()])
    last_name = StringField("Input your Last Name", validators=[DataRequired()])
    title = SelectField("Select Title", coerce=int, validators=[InputRequired()])
    role = SelectField("Select Role", coerce=int, validators=[InputRequired()])
    email = EmailField("Input your Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


def userform_instance(form_request=None):
    """
    Create to dynamically populate title, role inputs to selector elements
    """
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

    building_number = IntegerField(
        "Input the building number", validators=[DataRequired()]
    )
    building_name = StringField("Provide buiding name", validators=[DataRequired()])
    building_description = StringField(
        "Building Description", validators=[InputRequired()]
    )
    submit = SubmitField("Submit")


class CreateRoomForm(FlaskForm):
    """
    Room Form fields
    """

    space_number_id = StringField("Input the space id", validators=[DataRequired()])
    building_number = SelectField(
        "Provide buiding name", coerce=int, validators=[DataRequired()]
    )
    floor_number = IntegerField("Provide floor number", validators=[DataRequired()])
    wing_number = IntegerField("Provide wing number", validators=[DataRequired()])
    room_number = IntegerField("Provide room number", validators=[DataRequired()])
    room_type = SelectField(
        "Provide the room type", coerce=int, validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


def spaceform_instance(form_request=None):
    """
    Create to dynamically populate room type and building inputs to selector elements
    """
    user_form = CreateRoomForm(form_request)

    room_type_results = RoomClassification.query.order_by(
        RoomClassification.room_type_id.desc()
    ).all()
    room_type_query_list = [
        (i.room_type_id, i.room_type.title()) for i in room_type_results
    ]
    room_options = room_type_query_list
    user_form.room_type.choices = room_options

    building_results = Buildings.query.order_by(Buildings.building_name.asc()).all()
    building_query_list = [
        (i.building_number, i.building_name.title()) for i in building_results
    ]
    user_form.building_number.choices = building_query_list

    return user_form


class CreateTitleForm(FlaskForm):
    """
    Title Form fields
    """

    title = StringField("Input a new title", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateRolesForm(FlaskForm):
    """
    Roles Form fields
    """

    user_role = StringField("Input a new role", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateRoomClassificationForm(FlaskForm):
    """
    Room Classification Form fields
    """

    room_type = StringField("Input a new room type", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateRoomAmenitiesForm(FlaskForm):
    """
    Room Amenities Form fields
    """

    space_number_id = SelectField(
        "Select Room", coerce=int, validators=[DataRequired()]
    )
    room_projector = StringField("Room includes projector", validators=[DataRequired()])
    room_seating = StringField("Input number of seats", validators=[DataRequired()])
    submit = SubmitField("Submit")


def amenities_form_instance(form_request=None):
    """
    Create to dynamically populate amenities
    """
    amenities_form = CreateRoomAmenitiesForm(form_request)

    amenities_results = (
        Rooms.select(Rooms.space_number_id)
        .query.order_by(Rooms.space_number_id.desc())
        .all()
    )
    amenities_query_list = [i.title() for i in amenities_results]

    amenities_form.room_type.choices = amenities_query_list

    return amenities_form


class CreateRequestsForm(FlaskForm):
    """
    Request Form fields
    """

    # autofill in with logged in user id - login_user_id = current_user.get_id()
    # Select Building, floor, room
    building_number = SelectField(
        "Select building name", coerce=int, validators=[DataRequired()]
    )
    floor = SelectField("Select floor", coerce=int, validators=[DataRequired()])
    wing = SelectField("Select wing", coerce=int, validators=[DataRequired()])
    room = SelectField("Select room", coerce=int, validators=[DataRequired()])
    # Calc remaining options for wing for user to select
    # calc space_number_id in the background
    # calc available access approver for user to select
    access_approver_id = SelectField(
        "Select approver", coerce=int, validators=[DataRequired()]
    )
    # access_code_id = calculate behind the scene
    # status_code = calculate as default of "Waiting for Approval"
    # request_date = calculated based on submit datetime
    # approved_date = keep null
    # approved = calculate as False
    # add requestor_comment as a new field
    # approval_comment = keep null
    # rejection_comment = keep null

    submit = SubmitField("Submit")


def request_form_instance(form_request=None):
    """
    Create to dynamically update requests form
    """
    request_form = CreateRequestsForm(form_request)

    building_numbers = (
        Buildings.select(Buildings.building_number, Buildings.building_name)
        .query.order_by(Buildings.building_name.desc())
        .all()
    )
    building_list = [
        (i.building_number, i.building_name.title()) for i in building_numbers
    ]
    request_form.room_type.choices = building_list

    # for these simple queries can I convert the slalchemy object to a list with .to_list()
    floor_numbers = (
        Rooms.select(Rooms.floor_number).query.order_by(Rooms.floor_number.desc()).all()
    )
    floor_list = [i for i in floor_numbers]
    request_form.type.choices = floor_list

    wing_numbers = (
        Rooms.select(Rooms.wing_number).query.order_by(Rooms.wing_number.desc()).all()
    )
    wing_list = [i for i in wing_numbers]
    request_form.type.choices = wing_list

    room_numbers = (
        Rooms.select(Rooms.room_number).query.order_by(Rooms.room_number.desc()).all()
    )
    room_list = [i for i in room_numbers]
    request_form.type.choices = room_list

    approvers = Approvers.select(Approvers.approver_id).distinct().query.order_by(Approvers.approver_id).all()
    approver_list = [i for i in approvers]
    request_form.type.choices = approver_list 
    
    # I think this is the subquery that is needed get approver names
    # thsi should replace the approvers variable above
    subquery2 = ApproverZones.select(ApproverZones.access_approver_id.distinct()).query().filter(ApproverZones.building_number == 24).subquery()
    subquery1 = Approvers.select(Approvers.approver_id).query().filter(Approvers.access_approver_id.in_(subquery2)).subquery()
    query = Users.select(Users.first_name, Users.last_name).query().filter(Users.user_id.in_(subquery1))

    # Select first_name, last_name
    # From users 
    # Where user_id in (
    #     Select approver_id
    #     From access_approvers
    #     Where access_approver_id in (
    #         Select Distinct access_approver_id
    #         From approver_zones
    #         Where building_number = <form input>
    #     )
    # )

    return request_form


class CreateKeysForm(FlaskForm):
    """
    Keys Fabricated Form fields
    """

    key_number = SelectField(
        "Select key number", coerce=int, validators=[DataRequired()]
    )
    key_copy = StringField("Input key copy number", validators=[DataRequired()])
    access_code_id = SelectField(
        "Select access code", coerce=int, validators=[DataRequired()]
    )
    fabrication_status_id = 1  # set default to 'In queue'
    submit = SubmitField("Submit")


def keys_form_instance(form_request=None):
    """
    Create to dynamically update keys form
    """

    keys_form = CreateKeysForm(form_request)

    # add choices for key_Number, access_code dynamically

    return keys_form


class CreateKeyStatusForm(FlaskForm):
    """
    Key status form fields
    """

    key_status = StringField("Input new key status", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateKeyOrdersForm(FlaskForm):
    """
    Key order status form fields
    """

    # calc transaction_id from requests table - add behind the scenes
    access_code_id = StringField("Input new key status", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateKeyInventoryForm(FlaskForm):
    """
    Key inventory form fields
    """

    # calc transaction_id from requests table - add behind the scenes
    transaction_id = 1
    key_number = IntegerField("Input new key number", validators=[DataRequired()])
    key_copy = IntegerField("Input new key copy number", validators=[DataRequired()])
    date_transferred = 1  # set the date of the handoff
    date_returned = 1  # set to default of null
    submit = SubmitField("Submit")


class CreateApproversForm(FlaskForm):
    """
    Key approver form fields
    """

    # calc transaction_id from requests table - add behind the scenes
    access_approver_id = 1  # ???
    approver_id = 1  #
    role_approved_by = SelectField("Select approver name", validators=[DataRequired()])
    key_copy = IntegerField("Input new key copy number", validators=[DataRequired()])
    date_transferred = 1  # set the date of the handoff
    date_returned = 1  # set to default of null
    submit = SubmitField("Submit")
