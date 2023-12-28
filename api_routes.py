from flask import Blueprint, request, jsonify, Response, redirect, flash, session
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
    RoomAssignment,
    Titles,
    Roles,
    AccessPairs,
    Approvers,
    Zones,
    KeyInventory,
    KeyOrders,
    OrderStatus,
    KeysCreated,
    FabricationStatus,
    KeyStatus,
)
from forms import update_order_status_form_instance

from sqlalchemy.orm import aliased
from sqlalchemy import or_, func
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


# API Update Routes


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


@api.route("/orders/status/<request_id>", methods=["POST"])
@include_login_form
def order_status_update(request_id=None):
    update_order_form = update_order_status_form_instance(request.form)

    if update_order_form.validate_on_submit():
        update_record = KeyOrders.query.get(int(request_id))
        update_record.order_status_id = update_order_form.order_status_id.data
        db.session.commit()

        update_order_form.order_status_id.data = ""
        flash("Key Order Updated Successfully")

    return redirect(request.referrer)


@api.route("/orders/status/group", methods=["GET"])
@include_login_form
def order_status_group():
    records = (
        KeyInventory.query.with_entities(
            KeyStatus.key_status, func.count(KeyInventory.key_status_id)
        )
        .join(KeyStatus, KeyStatus.key_status_id == KeyInventory.key_status_id)
        .group_by(KeyStatus.key_status)
        .all()
    )

    data = []
    for record in records:
        # data.append({name: getattr(record, name) for name in column_names})
        # column_names = Requests.__table__.columns.keys()

        data.append(
            {
                "Key Status": record[0],
                "Number Keys": record[1],
            }
        )

    return jsonify(data)


# API table routes


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


@api.route("/table/users/group", methods=["GET"])
@include_login_form
def users_grouped_table():
    """
    Route used to get all users access
    """

    records = (
        Users.query.with_entities(
            Users.user_id,
            Users.first_name,
            Users.last_name,
            Users.email,
            Requests.space_number_id,
        )
        .join(Requests, Requests.user_id == Users.user_id)
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
                "Email": record[3],
                "Accessible Spaces": record[4],
            }
        )

    df = pd.DataFrame(data)

    users_and_spaces = (
        df.groupby(["User ID", "First Name", "Last Name", "Email"])["Accessible Spaces"]
        .apply(lambda x: ", ".join(x))
        .reset_index()
    )
    data = users_and_spaces.to_dict(orient="records")

    return jsonify(data)


@api.route("/table/buildings/group", methods=["GET"])
@include_login_form
def buildings_grouped_table():
    """
    Route used to get all building access
    """

    records = (
        Users.query.with_entities(
            Users.user_id,
            Users.first_name,
            Users.last_name,
            Users.email,
            Requests.space_number_id,
            RoomClassification.room_type,
        )
        .join(Requests, Requests.user_id == Users.user_id)
        .join(Rooms, Rooms.space_number_id == Requests.space_number_id)
        .join(RoomClassification, RoomClassification.room_type_id == Rooms.room_type_id)
        .order_by(Users.last_name)
        .all()
    )

    data = []
    for record in records:
        data.append(
            {
                "Room": record[4],
                "Room Type": record[5].title(),
                "People With Access": f"{record[1].title()} {record[2].title()} - {record[3]}",
            }
        )

    df = pd.DataFrame(data)

    users_and_spaces = (
        df.groupby(["Room", "Room Type"])["People With Access"]
        .apply(lambda x: "<br> ".join(x))
        .reset_index()
    )
    data = users_and_spaces.to_dict(orient="records")

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


@api.route("/table/inventory", methods=["GET"])
@include_login_form
def inventory_table():
    records = (
        KeyInventory.query.with_entities(
            KeyInventory.access_code_id, func.count(KeyInventory.access_code_id)
        )
        .filter(KeyInventory.key_status_id == 2)
        .group_by(KeyInventory.access_code_id)
        .all()
    )

    data = []
    for record in records:
        data.append({"Key": record[0], "Keys Available": record[1]})

    return jsonify(data)


@api.route("/table/orders", methods=["GET"])
@include_login_form
def orders_table():
    records = (
        KeyOrders.query.with_entities(
            KeyOrders.access_code_id,
            OrderStatus.order_status,
            Users.first_name,
            Users.last_name,
            Users.email,
            Requests.request_date,
            KeyOrders.request_id,
            KeyOrders.date_key_received,
        )
        .distinct()
        .join(OrderStatus, OrderStatus.order_status_id == KeyOrders.order_status_id)
        .join(Requests, Requests.request_id == KeyOrders.request_id)
        .join(Users, Users.user_id == Requests.user_id)
        .filter(KeyOrders.order_status_id < 4)
        .order_by(KeyOrders.request_id.asc())
        .all()
    )

    data = []
    for record in records:
        data.append(
            {
                "Request #": record[6],
                "Ordered Key": record[0],
                "Status": record[1],
                "Name": f"{record[2].title()} {record[3].title()}",
                "Email": record[4],
                "Request Date": record[5],
                "Date Ready for Pickup": record[7],
            }
        )

    return jsonify(data)


@api.route("/table/keyshop", methods=["GET"])
@include_login_form
def keyshop_table():
    records = (
        KeysCreated.query.with_entities(
            KeysCreated.request_id,
            KeysCreated.access_code_id,
            KeysCreated.key_copy,
            FabricationStatus.fabrication_status,
            Users.first_name,
            Users.last_name,
        )
        .distinct()
        .join(
            FabricationStatus,
            FabricationStatus.fabrication_status_id
            == KeysCreated.fabrication_status_id,
        )
        .join(Users, Users.user_id == KeysCreated.key_maker_user_id)
        .filter(KeysCreated.fabrication_status_id < 3)
        .order_by(KeysCreated.request_id.asc())
        .all()
    )

    data = []
    for record in records:
        data.append(
            {
                "Request #": record[0],
                "Access Code": record[1],
                "Key Copy": record[2],
                "Fabrication Status": record[3],
                "Key Maker": f"{record[4].title()} {record[5].title()}",
            }
        )

    return jsonify(data)


# testing new api


@api.route("/new", methods=["GET"])
@include_login_form
def new():
    """
    Used to test request logic for route 'site/post/basket/add'
    """
    results = AccessPairs.query.all()
    data = []
    for result in results:
        data.append(
            {"Access Code": result.access_code_id, "space_id": result.space_number_id}
        )

    df = pd.DataFrame(data)

    pivot_table = pd.crosstab(df["Access Code"], df.space_id)

    results = []
    for row in pivot_table.iterrows():
        access_code = row[0]
        s = row[1]
        included_rooms = s[s > 0]
        rooms = list(included_rooms.index)
        total_rooms = len(rooms)

        dict = {"id": access_code, "value": tuple(rooms), "count": total_rooms}

        results.append(dict)

    print(results)

    return jsonify(results)


@api.route("/building/info/<building>", methods=["GET"])
@include_login_form
def request_room_filter(building):
    """
    Used to retrieve data to update dropdown menus
    as seen in formFieldUpdate.js
    """
    records = Rooms.query.filter(Rooms.building_number == building)

    column_names = Rooms.__table__.columns.keys()
    data = []
    for record in records:
        data.append({name: getattr(record, name) for name in column_names})

    wings = set()
    floors = set()
    rooms = set()
    structure = dict()
    for i in data:
        if i["wing_number"] not in wings:
            wings.add(i["wing_number"])
            floors.add(i["floor_number"])
            rooms.add(i["room_number"])
            structure["wing"] = {
                str(i["wing_number"]): {
                    "floor": {str(i["floor_number"]): [i["room_number"]]}
                }
            }
        else:
            if i["floor_number"] not in floors:
                floors.add(i["floor_number"])
                rooms.add(i["room_number"])
                structure["wing"][str(i["wing_number"])]["floor"][
                    str(i["floor_number"])
                ] = [i["room_number"]]
            else:
                if i["room_number"] not in rooms:
                    rooms.add(i["room_number"])
                    structure["wing"][str(i["wing_number"])]["floor"][
                        str(i["floor_number"])
                    ].append(i["room_number"])
                else:
                    continue

    structure["wings"] = list(wings)
    structure["wing"][str(i["wing_number"])]["floors"] = list(floors)

    print(structure)
    return jsonify(structure)


@api.route("/approver/info/<building_number>", methods=["GET"])
@include_login_form
def request_approver_filter(building_number):
    """
    Used to retrieve data to update dropdown menus
    as seen in formFieldUpdate.js
    """
    building_approver = (
        Zones.query.with_entities(
            Zones.approver_id, Users.first_name, Users.last_name, Users.email
        )
        .distinct()
        .join(Approvers, Approvers.approver_id == Zones.approver_id)
        .join(Users, Users.user_id == Approvers.user_id)
        .filter(Zones.building_number == building_number)
    )

    approver_list = [
        {
            "approver_id": i.approver_id,
            "name": f"{i.first_name.title()} {i.last_name.title()} - ({i.email})",
        }
        for i in building_approver
    ]

    return jsonify(approver_list)


@api.route("/assignment/info/<space_number>", methods=["GET"])
@include_login_form
def request_assignee_filter(space_number):
    """
    Used to retrieve data to update dropdown menus
    as seen in formFieldUpdate.js
    """
    space_assignee = (
        RoomAssignment.query.with_entities(
            RoomAssignment.user_id, Users.first_name, Users.last_name, Users.email
        )
        .join(Users, Users.user_id == RoomAssignment.user_id)
        .filter(RoomAssignment.space_number_id == space_number)
    )

    assignee_list = [
        {
            "user_id": i.user_id,
            "name": f"{i.first_name.title()} {i.last_name.title()} - ({i.email})",
        }
        for i in space_assignee
    ]

    return jsonify(assignee_list)
