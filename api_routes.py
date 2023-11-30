from flask import Blueprint, request, jsonify, Response
import json
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
    AccessPairs,
    Approvers,
    Zones,
)
from sqlalchemy.orm import aliased
from sqlalchemy import or_
from flask_login import current_user
import pandas as pd

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
            .filter(Requests.user_id == login_user_id, Requests.request_status_id < 6)
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
            .filter(
                Requests.user_id == login_user_id,
                or_(Requests.request_status_id == 6, Requests.request_status_id == 7),
            )
            .join(
                RequestStatus,
                RequestStatus.request_status_id == Requests.request_status_id,
            )
            .join(Users, Users.user_id == Requests.user_id)
            .all()
        )

        # print(records)
        # if not records:
        #     print(json.dumps([{"Title": "Response"}]))
        #     return json.dumps([{"Status": "No keys appear to be issued at this time."}])

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


@api.route("/key/lost/<lost_id>", methods=["GET"])
@api.route("/key/return/<return_id>")
@include_login_form
def key_status_update(lost_id=None, return_id=None):
    if lost_id:
        status_id = 9
        request_id = lost_id
    elif return_id:
        status_id = 7
        request_id = return_id
    else:
        print("something went wrong")

    record = Requests.query.get(request_id)
    record.request_status_id = status_id
    db.session.commit()

    return Response(status=204)


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


@api.route("/table/matrix/", methods=["GET"])
@include_login_form
def matrix_table():
    results = AccessPairs.query.all()
    data = []
    for result in results:
        data.append(
            {"Access Code": result.access_code_id, "space_id": result.space_number_id}
        )

    df = pd.DataFrame(data)

    pivot_table = pd.crosstab(df["Access Code"], df.space_id)
    pivot_table = pivot_table.astype(str)
    pivot_table.iloc[0:, 0:] = pivot_table.iloc[0:, 0:].replace({"1": "X"})
    pivot_table.iloc[0:, 0:] = pivot_table.iloc[0:, 0:].replace({"0": ""})
    data = pivot_table.reset_index().to_dict(orient="records")

    return jsonify(data)


@api.route("/table/approver", methods=["GET"])
@include_login_form
def approver_table():
    Users_alias_user_id = aliased(Users)
    Users_alias_approved_by = aliased(Users)
    results = (
        Approvers.query.with_entities(
            Approvers.approver_id,
            Approvers.user_id,
            Users_alias_user_id.first_name.label("f_name"),
            Users_alias_user_id.last_name.label("l_name"),
            Users_alias_user_id.email,
            Users_alias_approved_by.first_name,
            Users_alias_approved_by.last_name,
            Approvers.date_approved,
            Approvers.date_removed,
        )
        .join(Users_alias_user_id, Users_alias_user_id.user_id == Approvers.user_id)
        .join(
            Users_alias_approved_by,
            Users_alias_approved_by.user_id == Approvers.role_approved_by,
        )
        .all()
    )
    data = []
    for result in results:
        data.append(
            {
                "Approver ID": result.approver_id,
                "User ID": result.user_id,
                "Approver Name": f"{result.f_name.title()} {result.l_name.title()}",
                "Approver Email": result.email,
                "System Approver ": f"{result.first_name.title()} {result.last_name.title()}",
                "Date Approved": result.date_approved,
                "Date Removed": result.date_removed,
            }
        )

    return jsonify(data)


@api.route("/table/zones", methods=["GET"])
@include_login_form
def zone_table():
    results = (
        Zones.query.with_entities(
            Zones.building_number,
            Buildings.building_name,
            Users.first_name,
            Users.last_name,
            Users.email,
        )
        .join(Buildings, Buildings.building_number == Zones.building_number)
        .join(Approvers, Approvers.approver_id == Zones.approver_id)
        .join(Users, Users.user_id == Approvers.user_id)
        .all()
    )
    data = []
    for result in results:
        data.append(
            {
                "Approver Name": f"{result.first_name.title()} {result.last_name.title()} - {result.email}<br>",
                "Approver Email": result.email,
                "Building": result.building_name,
            }
        )

    df = pd.DataFrame(data)
    building_approvers = (
        df.groupby("Building")["Approver Name"]
        .apply(lambda x: ", ".join(x))
        .reset_index()
    )
    data = building_approvers.to_dict(orient="records")

    return jsonify(data)
