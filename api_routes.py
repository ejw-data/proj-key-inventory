from flask import Blueprint, request, redirect, render_template, flash, jsonify
from models import (
    db,
    Requests,
    RequestStatus,
    Users,
    Buildings,
    Rooms,
    RoomClassification,
    RoomAmenities,
    Titles,
    Roles,
)
from flask_login import current_user

api = Blueprint("api", __name__, url_prefix="/api")


def logged_in_user():
    return current_user.get_id()


# views to include additional_parameters()
# collect route function names.  Note:  "site." is needed becasue using blueprints
login_form_views = []


def include_login_form(fn):
    login_form_views.append("api." + fn.__name__)
    return fn


# ---------------------------------------------------------- #
# Universal routes
# ---------------------------------------------------------- #

# API routes


@api.route("/table/requests/<active>", methods=["GET"])
@include_login_form
def request_table(active):
    """
    Route used to get current user information
    """
    login_user_id = logged_in_user()
    # column_names = Requests.__table__.columns.keys()
    # column_names = [
    #     "request_id",
    #     "user_id",
    #     "space_number_id",
    #     "approved",
    #     "request_status_name",
    # ]

    if active == "all":
        records = (
            Requests.query.with_entities(
                Requests.request_id,
                Users.first_name,
                Users.last_name,
                Requests.space_number_id,
                Requests.approved,
                RequestStatus.request_status_name,
            )
            .filter(Requests.user_id == login_user_id)
            .join(
                RequestStatus,
                RequestStatus.request_status_id == Requests.request_status_id,
            )
            .join(Users, Users.user_id == Requests.user_id)
            .all()
        )

    elif active == "active":
        records = (
            Requests.query.with_entities(
                Requests.request_id,
                Users.first_name,
                Users.last_name,
                Requests.space_number_id,
                Requests.approved,
                RequestStatus.request_status_name,
            )
            .filter(Requests.user_id == login_user_id, Requests.request_status_id != 6)
            .join(
                RequestStatus,
                RequestStatus.request_status_id == Requests.request_status_id,
            )
            .join(Users, Users.user_id == Requests.user_id)
            .all()
        )

    elif active == "inactive":
        records = (
            Requests.query.with_entities(
                Requests.request_id,
                Users.first_name,
                Users.last_name,
                Requests.space_number_id,
                Requests.approved,
                RequestStatus.request_status_name,
            )
            .filter(Requests.user_id == login_user_id, Requests.request_status_id == 6)
            .join(
                RequestStatus,
                RequestStatus.request_status_id == Requests.request_status_id,
            )
            .join(Users, Users.user_id == Requests.user_id)
            .all()
        )

    data = []
    for record in records:
        # data.append({name: getattr(record, name) for name in column_names})
        if active == "all":
            data.append(
                {
                    "Request ID": record[0],
                    "User Name": f"{record[1].title()} {record[2].title()}",
                    "Room Code": record[3],
                    "Approval Status": "Approved" if bool(record[4]) else "PENDING",
                    "Request Status": record[5],
                }
            )
        else:
            data.append(
                {
                    "Request ID": record[0],
                    "Room Code": record[3],
                    "Approval Status": "Approved" if bool(record[4]) else "PENDING",
                    "Request Status": record[5],
                }
            )

    return jsonify(data)


@api.route("/table/rooms/", methods=["GET"])
@include_login_form
def room_table():
    """
    Route used to get current room information
    """

    records = (
        Rooms.query.with_entities(
            Rooms.space_number_id,
            Buildings.building_name,
            Rooms.building_number,
            Rooms.wing_number,
            Rooms.floor_number,
            Rooms.room_number,
            RoomClassification.room_type,
            RoomAmenities.room_projector,
            RoomAmenities.room_seating,
        )
        .join(Buildings, Buildings.building_number == Rooms.building_number)
        .join(RoomClassification, RoomClassification.room_type_id == Rooms.room_type_id)
        .join(RoomAmenities, RoomAmenities.space_number_id == Rooms.space_number_id)
        .all()
    )

    data = []
    for record in records:
        data.append(
            {
                "Space ID": record[0],
                "Building Name": record[1],
                "Building Number": record[2],
                "Wing Number": record[3],
                "Floor Number": record[4],
                "Room Number": record[5],
                "Room Type": record[6].title(),
                "Room Projector": "Yes" if bool(record[7]) else "No",
                "Room Seating": record[8],
            }
        )

    return jsonify(data)


@api.route("/table/users/", methods=["GET"])
@include_login_form
def users_table():
    """
    Route used to get current user information
    """

    records = (
        Users.query.with_entities(
            Users.user_id,
            Users.first_name,
            Users.last_name,
            Titles.title,
            Roles.user_role,
            Users.email,
        )
        .join(Titles, Titles.title_id == Users.title_id)
        .join(Roles, Roles.role_id == Users.role_id)
        .order_by(Users.last_name)
        .all()
    )

    data = []
    for record in records:
        data.append(
            {
                "User ID": record[0],
                "First Name": record[1].title(),
                "Last Name": record[2].title(),
                "Title": record[3].title(),
                "Role": record[4].title(),
                "Email": record[5],
            }
        )

    return jsonify(data)
