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
from models import (
    Roles,
    Titles,
    RoomClassification,
    Buildings,
    Rooms,
    Approvers,
    Users,
    AccessCodes,
    OrderStatus,
    RoomAssignment,
)


# add data to access_approvers table
class CreateApproversForm(FlaskForm):
    """
    Key approver form fields
    """

    approver_id = SelectField("Select approver name", validators=[DataRequired()])
    role_approved_by = SelectField("Select approver name", validators=[DataRequired()])
    submit = SubmitField("Submit")


def approver_instance(form_request=None):
    """
    Create access approvers form
    Make results distinct
    """

    approver_form = CreateApproversForm(form_request)

    subquery = (
        Approvers.query.with_entities(Approvers.user_id)
        .distinct()
        .order_by(Approvers.user_id.asc())
    )
    approvers = (
        Users.query.with_entities(
            Users.first_name, Users.last_name, Approvers.approver_id, Users.email
        )
        .distinct(Users.first_name, Users.last_name)
        .order_by(Users.last_name.asc())
        .filter(Users.user_id.in_(subquery))
        .join(Approvers, Approvers.user_id == Users.user_id)
        .all()
    )

    approvers_list = [(-1, "Select access approver")] + [
        (
            i.approver_id,
            f"{i.first_name.title()} {i.last_name.title()} - {i.email}",
        )
        for i in approvers
    ]
    approver_form.role_approved_by.choices = approvers_list

    approver_candidates = (
        Users.query.with_entities(
            Users.user_id, Users.first_name, Users.last_name, Users.email
        )
        .distinct(Users.first_name, Users.last_name)
        .order_by(Users.last_name.asc())
        .filter(Users.user_id.not_in([3, 4]))
        .all()
    )
    approveable_list = [(-1, "Select general user")] + [
        (i.user_id, f"{i.first_name.title()} {i.last_name.title()} - {i.email}")
        for i in approver_candidates
    ]

    approver_form.approver_id.choices = approveable_list

    return approver_form


# add data to access_codes table
class CreateAccessCodesForm(FlaskForm):
    """
    Access codes form fields
    """

    access_description = StringField("Access description", validators=[DataRequired()])
    authorized_by = SelectField(
        "Select building manager requestor", validators=[DataRequired()]
    )
    # created_by is automatically filled in by using current_user
    # created_on is automatically filled in via postgres defaults
    # the code id is autogenerated
    submit = SubmitField("Submit")


# add data to access_pairs table
class CreateAccessPairsForm(FlaskForm):
    """
    Spaces accessible per access code
    """

    # status code id is autogenerated
    access_code_id = SelectField(
        "Select access code", coerce=int, validators=[DataRequired()]
    )
    space_number_id_fk = SelectField(
        "Select space to add to access code", coerce=str, validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


def access_pair_instance(form_request=None):
    """
    Created to dynamically update access
    """

    access_form = CreateAccessPairsForm(form_request)

    # found in other places
    space_results = (
        Rooms.query.with_entities(
            Rooms.space_number_id,
            Buildings.building_name,
            Rooms.floor_number,
            Rooms.room_number,
            Rooms.building_number,
        )
        .order_by(Rooms.space_number_id.asc())
        .join(Buildings, Buildings.building_number == Rooms.building_number)
        .all()
    )

    space_list = [("void", "Select space")] + [
        (
            i.space_number_id,
            f"{i.building_name} {i.floor_number}{str(i.room_number).zfill(2)} ({i.space_number_id})",
        )
        for i in space_results
    ]

    access_form.space_number_id_fk.choices = space_list

    access_id = (
        AccessCodes.query.with_entities(AccessCodes.access_code_id)
        .order_by(AccessCodes.access_code_id.asc())
        .all()
    )
    access_list = [(-1, "Select access code")] + [
        (i.access_code_id, i.access_code_id) for i in access_id
    ]
    access_form.access_code_id.choices = access_list

    return access_form


# add data to approval_status table
class CreateRequestStatusForm(FlaskForm):
    """
    Approval status form fields
    """

    # status code id is autogenerated
    request_status_name = StringField("Add status code", validators=[DataRequired()])
    submit = SubmitField("Submit")


# add data to approver_zones table
class CreateZonesForm(FlaskForm):
    """
    Building manager approval areas
    """

    # status code id is autogenerated
    building_number_fk = SelectField(
        "Select building",
        choices=[(24, "Silverman Hall"), (44, "Ford")],
        validators=[DataRequired()],
    )
    approver_id_fk = SelectField("Select building manager", validators=[DataRequired()])
    submit = SubmitField("Submit")


def zones_instance(form_request=None):
    """
    Create to dynamically update keys form
    """

    zones_form = CreateZonesForm(form_request)

    buildings = (
        Buildings.query.with_entities(
            Buildings.building_number, Buildings.building_name
        )
        .order_by(Buildings.building_name.asc())
        .all()
    )
    buildings_list = [(-1, "Select building")] + [
        (i.building_number, f"{i.building_name.title()} - ({i.building_number})")
        for i in buildings
    ]
    zones_form.building_number_fk.choices = buildings_list

    subquery = (
        Approvers.query.with_entities(Approvers.approver_id)
        .distinct()
        .order_by(Approvers.approver_id.asc())
    )
    approvers = (
        Users.query.with_entities(
            Users.first_name, Users.last_name, Approvers.approver_id, Users.email
        )
        .order_by(Users.last_name.asc())
        .filter(Users.user_id.in_(subquery))
        .join(Approvers, Approvers.approver_id == Users.user_id)
        .all()
    )

    approvers_list = [(-1, "Select approver")] + [
        (
            i.approver_id,
            f"{i.first_name.title()} {i.last_name.title()} - {i.email}",
        )
        for i in approvers
    ]
    zones_form.approver_id_fk.choices = approvers_list

    return zones_form


# verify data and add data to authentication table
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


# add data to buildings table
class CreateBuildingForm(FlaskForm):
    """
    Building Form fields
    """

    building_number = IntegerField(
        "Input the building number", validators=[DataRequired()]
    )
    building_name = StringField("Provide building name", validators=[DataRequired()])
    building_description = StringField(
        "Building description", validators=[InputRequired()]
    )
    submit = SubmitField("Submit")


# add data to fabrication status table
class CreateFabricationStatusForm(FlaskForm):
    """
    Key shop status messages
    """

    # status code id is autogenerated
    fabrication_status = StringField(
        "Add fabrication status", validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


# add data to key_inventory table
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


# add data to key_status table
class CreateKeyStatusForm(FlaskForm):
    """
    Key status form fields
    """

    key_status = StringField("Input new key status", validators=[DataRequired()])
    submit = SubmitField("Submit")


# add data to keys_created table
class CreateKeysForm(FlaskForm):
    """
    Key Fabrication Form fields
    """

    key_number = SelectField(
        "Select key number", coerce=int, validators=[DataRequired()]
    )
    key_copy = StringField("Input key copy number", validators=[DataRequired()])
    access_code_id = SelectField(
        "Select access code", coerce=int, validators=[DataRequired()]
    )
    # fabrication_status_id =
    submit = SubmitField("Submit")


def keys_form_instance(form_request=None):
    """
    Create to dynamically update keys form
    """

    keys_form = CreateKeysForm(form_request)

    # add choices for key_Number, access_code dynamically

    return keys_form


# add data to requests table
# moved this table to the end of the file


# add data to roles table
class CreateRolesForm(FlaskForm):
    """
    Roles Form fields
    """

    user_role = StringField("Input a new role", validators=[DataRequired()])
    submit = SubmitField("Submit")


# add data to room_amenities table
class CreateRoomAmenitiesForm(FlaskForm):
    """
    Room Amenities Form fields
    """

    space_amenities = SelectField(
        "Select Room", coerce=str, validators=[DataRequired()]
    )
    room_projector = SelectField(
        "Room includes projector",
        choices=[(-1, "Make Selection"), (0, "False"), (1, "True")],
        coerce=int,
    )
    room_seating = IntegerField("Input number of seats", validators=[DataRequired()])
    submit = SubmitField("Submit")


def amenities_form_instance(form_request=None):
    """
    Create to dynamically populate amenities
    """
    amenities_form = CreateRoomAmenitiesForm(form_request)

    space_results = (
        Rooms.query.with_entities(
            Rooms.space_number_id,
            Buildings.building_name,
            Rooms.floor_number,
            Rooms.room_number,
            Rooms.building_number,
        )
        .order_by(Rooms.space_number_id.asc())
        .join(Buildings, Buildings.building_number == Rooms.building_number)
        .all()
    )

    space_list = [
        (
            i.space_number_id,
            f"{i.building_name} {i.floor_number}{str(i.room_number).zfill(2)} ({i.space_number_id})",
        )
        for i in space_results
    ]
    amenities_form.space_amenities.choices = [(-1, "Select Room")] + space_list

    return amenities_form


# add data to room_classification table
class CreateRoomClassificationForm(FlaskForm):
    """
    Room Classification Form fields
    """

    room_type_id = IntegerField("Input room type code", validators=[DataRequired()])
    room_type_name = StringField("Input a new room name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# add data to rooms table
class CreateRoomForm(FlaskForm):
    """
    Room Form fields
    """

    # space_number_id = StringField("Input the space id", validators=[DataRequired()])
    room_building_number = SelectField(
        "Provide building name", coerce=int, validators=[DataRequired()]
    )
    wing_number = StringField("Provide wing number", validators=[DataRequired()])
    floor_number = IntegerField("Provide floor number", validators=[DataRequired()])
    room_number = IntegerField("Provide room number", validators=[DataRequired()])
    room_type_id_fk = SelectField(
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

    user_form.room_type_id_fk.choices = [(-1, "Select Title")] + room_type_query_list

    building_results = Buildings.query.order_by(Buildings.building_name.asc()).all()
    building_query_list = [(-1, "Select Building")] + [
        (i.building_number, f"{i.building_name.title()} - ({i.building_number})")
        for i in building_results
    ]
    user_form.room_building_number.choices = building_query_list

    return user_form


# add data to titles table
class CreateTitleForm(FlaskForm):
    """
    Title Form fields
    """

    title = StringField("Input a new title", validators=[DataRequired()])
    submit = SubmitField("Submit")


# add data to users table
class CreateUserForm(FlaskForm):
    """
    User Form fields
    """

    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    title_fk = SelectField("Select title", coerce=int, validators=[InputRequired()])
    role = SelectField("Select role", coerce=int, validators=[InputRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    sponsor_id = SelectField(
        "Select PI or Supervisor", coerce=int, validators=[InputRequired()]
    )
    submit = SubmitField("Submit")


def userform_instance(form_request=None):
    """
    Create to dynamically populate title, role inputs to selector elements
    """
    user_form = CreateUserForm(form_request)

    title_results = Titles.query.order_by(Titles.title_id.desc()).all()
    title_query_list = [(-1, "Select title")] + [
        (i.title_id, i.title.title()) for i in title_results
    ]
    user_form.title_fk.choices = title_query_list

    sponsors = (
        Users.query.with_entities(
            Users.first_name, Users.last_name, Users.user_id, Users.email
        )
        .order_by(Users.last_name.asc())
        .filter(Users.role_id in [4, 5, 6])
        .all()
    )

    sponsor_list = [(-1, "Select approver")] + [
        (
            i.user_id,
            f"{i.first_name.title()} {i.last_name.title()} - {i.email}",
        )
        for i in sponsors
    ]
    user_form.sponsor_id.choices = sponsor_list

    role_results = Roles.query.order_by(Roles.role_id.desc()).all()
    role_query_list = [(-1, "Select role")] + [
        (i.role_id, i.user_role.title()) for i in role_results
    ]
    user_form.role.choices = role_query_list

    return user_form


# add data to titles table
class CreateAccessCodesForm(FlaskForm):
    """
    Access Code Form fields
    """

    access_description = StringField(
        "Provide access description", validators=[DataRequired()]
    )
    authorized_by = SelectField(
        "Select authorizer", coerce=int, validators=[InputRequired()]
    )
    submit = SubmitField("Submit")


def access_code_form_instance(form_request=None):
    accesscode_form = CreateAccessCodesForm(form_request)

    subquery = (
        Approvers.query.with_entities(Approvers.user_id)
        .distinct()
        .order_by(Approvers.user_id.asc())
    )
    approvers = (
        Users.query.with_entities(
            Users.first_name, Users.last_name, Approvers.approver_id
        )
        .order_by(Users.last_name.asc())
        .filter(Users.user_id.in_(subquery))
        .join(Approvers, Approvers.user_id == Users.user_id)
        .all()
    )

    approvers_list = [(-1, "Select approver")] + [
        (i.approver_id, f"{i.first_name.title()} {i.last_name.title()}")
        for i in approvers
    ]

    accesscode_form.authorized_by.choices = approvers_list

    return accesscode_form


# add data to requests table
# this table is moved to the end bc it is the most complicated
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
    assignment_id = SelectField(
        "Select PI/Manager of space", coerce=int, validators=[DataRequired()]
    )
    approver_id = SelectField(
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

    submit = SubmitField("Add Key")


def request_form_instance(form_request=None):
    """
    Create to dynamically update requests form
    """
    request_form = CreateRequestsForm(form_request)

    building_numbers = (
        Buildings.query.with_entities(
            Buildings.building_number, Buildings.building_name
        )
        .order_by(Buildings.building_name.asc())
        .all()
    )
    building_list = [(-1, "Select building")] + [
        (i.building_number, i.building_name.title()) for i in building_numbers
    ]
    request_form.building_number.choices = building_list

    floor_numbers = (
        Rooms.query.with_entities(Rooms.floor_number)
        .distinct()
        .order_by(Rooms.floor_number.asc())
        .all()
    )
    floor_list = [(-1, "Select floor")] + [
        (i.floor_number, i.floor_number) for i in floor_numbers
    ]
    request_form.floor.choices = floor_list

    wing_numbers = (
        Rooms.query.with_entities(Rooms.wing_number)
        .distinct()
        .order_by(Rooms.wing_number.asc())
        .all()
    )
    wing_list = [(-1, "Select wing")] + [
        (i.wing_number, i.wing_number) for i in wing_numbers
    ]
    request_form.wing.choices = wing_list

    room_numbers = (
        Rooms.query.with_entities(Rooms.room_number)
        .distinct()
        .order_by(Rooms.room_number.asc())
        .all()
    )
    room_list = [(-1, "Select room")] + [
        (i.room_number, i.room_number) for i in room_numbers
    ]
    request_form.room.choices = room_list

    subquery = (
        Approvers.query.with_entities(Approvers.user_id)
        .distinct()
        .order_by(Approvers.user_id.asc())
    )
    approvers = (
        Users.query.with_entities(
            Users.first_name, Users.last_name, Approvers.approver_id
        )
        .order_by(Users.last_name.asc())
        .filter(Users.user_id.in_(subquery))
        .join(Approvers, Approvers.user_id == Users.user_id)
        .all()
    )

    approvers_list = [(-1, "Select building approver")] + [
        (i.approver_id, f"{i.first_name.title()} {i.last_name.title()}")
        for i in approvers
    ]
    request_form.approver_id.choices = approvers_list

    # Add space owner query to autofill in the form
    space_assignments = (
        RoomAssignment.query.with_entities(Users.first_name, Users.last_name, Users.email, RoomAssignment.assignment_id)
        .distinct(Users.first_name, Users.last_name)
        .join(Rooms, Rooms.space_number_id == RoomAssignment.space_number_id)
        .join(Users, Users.user_id == RoomAssignment.user_id)
    )

    assignment_list = [(-1, "Select space authorizer")] + [
        (i.assignment_id, f"{i.first_name.title()} {i.last_name.title()} - ({i.email})")
        for i in space_assignments
    ]

    request_form.assignment_id.choices = assignment_list

    # I think this is the subquery that is needed get approver names
    # this should replace the approvers variable above
    # subquery2 = ApproverZones.select(ApproverZones.access_approver_id.distinct()).query().filter(ApproverZones.building_number == 24).subquery()
    # subquery1 = Approvers.select(Approvers.approver_id).query().filter(Approvers.access_approver_id.in_(subquery2)).subquery()
    # query = Users.select(Users.first_name, Users.last_name).query().filter(Users.user_id.in_(subquery1))

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


class CreateOrderStatusForm(FlaskForm):
    """
    Order Status Form fields
    """

    order_status = StringField("Input status", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateUpdateOrderStatusForm(FlaskForm):
    """
    Update Order Status
    """

    order_status_id = SelectField(
        "Select current status", coerce=int, validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


def update_order_status_form_instance(form_request=None):
    """
    Create to update orders status
    """
    order_status_form = CreateUpdateOrderStatusForm(form_request)

    status_options = OrderStatus.query.order_by(OrderStatus.order_status_id.asc()).all()

    order_status_list = [(-1, "Select order status")] + [
        (i.order_status_id, i.order_status.title()) for i in status_options
    ]

    order_status_form.order_status_id.choices = order_status_list

    return order_status_form
