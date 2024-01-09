import numpy as np
import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    session,
)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import (
    db,
    Approvers,
    AccessCodes,
    AccessPairs,
    RequestStatus,
    Zones,
    Authentication,
    Buildings,
    FabricationStatus,
    KeyInventory,
    # KeyOrders,
    KeyStatus,
    KeysCreated,
    OrderStatus,
    Requests,
    Roles,
    RoomAmenities,
    RoomClassification,
    Rooms,
    Titles,
    Users,
)
from query import get_access_code, get_profile
from access_codes import find_codes
from sqlalchemy import null, func

# from flask_sqlalchemy import SQLAlchemy
from forms import (
    LoginForm,
    RegisterForm,
    userform_instance,
    spaceform_instance,
    CreateBuildingForm,
    request_form_instance,
    amenities_form_instance,
    CreateRoomClassificationForm,
    CreateTitleForm,
    CreateRolesForm,
    keys_form_instance,
    CreateKeyStatusForm,
    CreateFabricationStatusForm,
    zones_instance,
    access_pair_instance,
    CreateRequestStatusForm,
    approver_instance,
    access_code_form_instance,
    CreateOrderStatusForm,
    update_order_status_form_instance,
)


# allow for multiple route types, see also api_routes.py
site = Blueprint("site", __name__)


# ---------- WIDELY USED PAGE PARAMETERS ----------------------------
def logged_in_user():
    return current_user.get_id()


# views to include additional_parameters()
# collect route function names.  Note:  "site." is needed becasue using blueprints
login_form_views = []


def include_login_form(fn):
    login_form_views.append("site." + fn.__name__)
    return fn


# used to pass parameters to menu banner
@site.context_processor
def additional_parameters():
    if request.endpoint not in login_form_views:
        return {}

    login_user_id = current_user.get_id()
    user_record = Users.query.filter_by(user_id=login_user_id).first()
    first_name = user_record.first_name.title()
    last_name = user_record.last_name.title()
    form = LoginForm()

    return {"first_name": first_name, "last_name": last_name, "form": form}


# ---------- PAGE ROUTES ----------------------------


@site.route("/dashboard")
@login_required
@include_login_form
def index():
    """
    Summary page for all users
    """

    profile = get_profile()

    request_form = request_form_instance()
    basket_form = request_form_instance()

    return render_template(
        "index.html",
        request_form=request_form,
        profile=profile,
        basket_form=basket_form,
    )


@site.route("/order-content")
@include_login_form
def ordercontent():
    return render_template("dynamic/_orders.html")


@site.route("/users")
@include_login_form
def users():
    """
    User information page, currently holds add users form
    """

    return render_template("users.html")


@site.route("/keys")
@include_login_form
def keys():
    """
    User information page, currently holds add users form
    """
    key_status_form = CreateKeyStatusForm()
    fabrication_form = CreateFabricationStatusForm()
    order_status_form = CreateOrderStatusForm()
    update_order_status_form = update_order_status_form_instance()

    # Table KeyOrders and KeyInventory should be filled via triggers

    return render_template(
        "keys.html",
        key_status_form=key_status_form,
        fabrication_form=fabrication_form,
        order_status_form=order_status_form,
        update_order_status_form=update_order_status_form,
    )


@site.route("/access")
@include_login_form
def access():
    """
    User information page, currently holds add users form
    """

    access_pair_form = access_pair_instance()
    access_code_form = access_code_form_instance()

    return render_template(
        "access.html",
        access_pair_form=access_pair_form,
        access_code_form=access_code_form,
    )


@site.route("/admin")
@include_login_form
def admin():
    """
    User information page, currently holds add users form
    """
    user_form = userform_instance()
    space_form = spaceform_instance()
    building_form = CreateBuildingForm()
    amenities_form = amenities_form_instance()
    room_type_form = CreateRoomClassificationForm()
    title_form = CreateTitleForm()
    role_form = CreateRolesForm()
    zone_form = zones_instance()
    approver_form = approver_instance()
    request_status_form = CreateRequestStatusForm()
    order_status_form = CreateOrderStatusForm()
    key_status_form = CreateKeyStatusForm()
    fab_status_form = CreateFabricationStatusForm()

    return render_template(
        "admin.html",
        user_form=user_form,
        space_form=space_form,
        building_form=building_form,
        amenities_form=amenities_form,
        room_type_form=room_type_form,
        title_form=title_form,
        role_form=role_form,
        zone_form=zone_form,
        approver_form=approver_form,
        request_status_form=request_status_form,
        order_status_form=order_status_form,
        key_status_form=key_status_form,
        fab_status_form=fab_status_form,
        # order_status not added yet
    )


# ---------- FORM ROUTES ----------------------------


# User Addition by Administrator
# maybe rename route /post/user/add
@site.route("/post/user/add", methods=["POST"])
@include_login_form
def add_user():
    """
    Route used to add users to database, applied on admin.html
    """
    user_form = userform_instance(request.form)

    if user_form.validate_on_submit():
        user_login_exists = Authentication.query.filter_by(
            username=user_form.email.data
        ).first()
        user_account_exists = Users.query.filter_by(email=user_form.email.data).first()

        if (user_login_exists is None) and (user_account_exists is None):
            user = Users(
                first_name=user_form.first_name.data,
                last_name=user_form.last_name.data,
                title_id=user_form.title_fk.data,
                role_id=user_form.role.data,
                email=user_form.email.data.lower(),
                sponsor_id=user_form.sponsor_id,
            )
            db.session.add(user)
            db.session.commit()

            user_form.first_name.data = ""
            user_form.last_name.data = ""
            user_form.title_fk.data = ""
            user_form.role.data = ""
            user_form.email = ""
            user_form.sponsor_id = ""
            flash("User Added Successfully")
        elif user_login_exists is not None:
            flash("User already has login and password.")
        elif user_account_exists is not None:
            flash(
                f"User has account but no password.  User needs to register with {user_form.email.data}."
            )
        else:
            flash("Error has occurred.  Contact key tracker administrator.")
    return redirect(request.referrer)


@site.route("/post/building/add", methods=["POST"])
@include_login_form
def add_buiding():
    """
    Route used to add buildings to database, applied on admin.html
    """
    user_form = CreateBuildingForm()

    if user_form.validate_on_submit():
        building = Buildings(
            building_number=user_form.building_number.data,
            building_name=user_form.building_name.data,
            building_description=user_form.building_description.data,
        )
        db.session.add(building)
        db.session.commit()

        user_form.building_number.data = ""
        user_form.building_name.data = ""
        user_form.building_description.data = ""
        flash("Building Added Successfully")

    return redirect(request.referrer)


@site.route("/post/room/add", methods=["POST"])
@include_login_form
def add_room():
    """
    Route used to add buildings to database, applied on admin.html
    """
    user_form = spaceform_instance(request.form)

    if user_form.validate_on_submit():
        room = Rooms(
            space_number_id=user_form.space_number_id.data,
            building_number=user_form.room_building_number.data,
            wing_number=user_form.wing_number.data,
            floor_number=user_form.floor_number.data,
            room_number=user_form.room_number.data,
            room_type=user_form.room_type.data,
        )
        db.session.add(room)
        db.session.commit()

        user_form.space_number_id.data = ""
        user_form.room_building_number.data = ""
        user_form.floor_number.data = ""
        user_form.wing_number.data = ""
        user_form.room_number.data = ""
        user_form.room_type.data = ""
        flash("Room Added Successfully")

    return redirect(request.referrer)


@site.route("/post/amenities/add", methods=["POST"])
@include_login_form
def add_amenities():
    """
    Route used to add room amenities to database, applied on admin.html
    """
    user_form = amenities_form_instance(request.form)

    if user_form.validate_on_submit():
        room_amenity = RoomAmenities(
            space_number_id=user_form.space_amenities.data,
            room_projector=user_form.room_projector.data,
            room_seating=user_form.room_seating.data,
        )
        db.session.add(room_amenity)
        db.session.commit()

        user_form.space_amenities.data = ""
        user_form.room_projector.data = ""
        user_form.room_seating.data = ""
        flash("Room Details Added Successfully")

    return redirect(request.referrer)


@site.route("/post/room/type/add", methods=["POST"])
@include_login_form
def add_room_type():
    """
    Route used to add room classifications to database, applied on admin.html
    """
    user_form = CreateRoomClassificationForm(request.form)

    if user_form.validate_on_submit():
        room_type = RoomClassification(
            room_type_id=user_form.room_type_id_fk.data,
            room_type=user_form.room_type_name.data.lower(),
        )
        db.session.add(room_type)
        db.session.commit()

        user_form.room_type_id_fk.data = ""
        user_form.room_type_name.data = ""
        flash("Room Type Added Successfully")

    return redirect(request.referrer)


@site.route("/post/title/add", methods=["POST"])
@include_login_form
def add_title():
    """
    Route used to add room classifications to database, applied on admin.html
    """
    user_form = CreateTitleForm()

    if user_form.validate_on_submit():
        title = Titles(
            title=user_form.title.data.lower(),
        )
        db.session.add(title)
        db.session.commit()

        user_form.title.data = ""
        flash("Title Added Successfully")

    return redirect(request.referrer)


@site.route("/post/role/add", methods=["POST"])
@include_login_form
def add_role():
    """
    Route used to add user role to database, applied on admin.html
    """
    user_form = CreateRolesForm()

    if user_form.validate_on_submit():
        user_role = Roles(
            user_role=user_form.user_role.data.lower(),
        )
        db.session.add(user_role)
        db.session.commit()

        user_form.user_role.data = ""
        flash("User Role Added Successfully")

    return redirect(request.referrer)


# no form yet
@site.route("/post/order/status/add", methods=["POST"])
@include_login_form
def add_orderstatus():
    """
    Route used to add order status role to database, applied on admin.html
    """
    user_form = CreateOrderStatusForm()

    if user_form.validate_on_submit():
        order_status = OrderStatus(
            order_status=user_form.order_status.data.upper(),
        )
        db.session.add(order_status)
        db.session.commit()

        user_form.user_role.data = ""
        flash("Order Status Added Successfully")

    return redirect(request.referrer)


@site.route("/post/key/add", methods=["POST"])
@include_login_form
def add_keys():
    """
    Route used to add keys to database, applied on admin.html
    """
    user_form = keys_form_instance(request.form)

    if user_form.validate_on_submit():
        key_copy = KeysCreated(
            key_number=user_form.key_number.data,
            key_copy=user_form.key_copy.data,
            access_code_id=user_form.access_code_id.data,
            # fabrication_status_id=user_form.fabrication_status_id.data,
        )
        db.session.add(key_copy)
        db.session.commit()

        user_form.key_number.data = ""
        user_form.key_copy.data = ""
        user_form.access_code_id.data = ""
        # user_form.fabrication_status_id.data = ""
        flash("Key Added Successfully")

    return redirect(request.referrer)


@site.route("/post/key/status/add", methods=["POST"])
@include_login_form
def add_keystatus():
    """
    Route used to add key status to database, applied on admin.html
    """
    user_form = CreateKeyStatusForm()

    if user_form.validate_on_submit():
        key_status = KeyStatus(
            key_status=user_form.key_status.data.upper(),
        )
        db.session.add(key_status)
        db.session.commit()

        user_form.key_status.data = ""
        flash("Key Status Added Successfully")

    return redirect(request.referrer)


@site.route("/post/fabrication/status/add", methods=["POST"])
@include_login_form
def add_fabricationstatus():
    """
    Route used to add fabrication status to database, applied on admin.html
    """
    user_form = CreateFabricationStatusForm()

    if user_form.validate_on_submit():
        fab_status = FabricationStatus(
            fabrication_status=user_form.fabrication_status.data.upper(),
        )
        db.session.add(fab_status)
        db.session.commit()

        user_form.fabrication_status.data = ""
        flash("Key Fabrication Status Added Successfully")

    return redirect(request.referrer)


@site.route("/post/request/status/add", methods=["POST"])
@include_login_form
def add_requeststatus():
    """
    Route used to add approval status to database, applied on admin.html
    """
    user_form = CreateRequestStatusForm()

    if user_form.validate_on_submit():
        approval_status = RequestStatus(
            status_code_name=user_form.status_code_name.data.upper(),
        )
        db.session.add(approval_status)
        db.session.commit()

        user_form.status_code_name.data = ""
        flash("Approval Status Added Successfully")

    return redirect(request.referrer)


@site.route("/post/zones/add", methods=["POST"])
@include_login_form
def add_spaceapprover():
    """
    Route used to add space approvers to database, applied on admin.html
    """
    user_form = zones_instance(request.form)

    if user_form.validate_on_submit():
        approver = Zones(
            building_number=user_form.building_number_fk.data,
            approver_id=user_form.approver_id_fk.data,
        )
        db.session.add(approver)
        db.session.commit()

        user_form.building_number_fk.data = ""
        user_form.approver_id_fk.data = ""
        flash("Space Approver Added Successfully")

    return redirect(request.referrer)


@site.route("/post/access/add", methods=["POST"])
@include_login_form
def add_accesspair():
    """
    Route used to add space assignments to database, applied on admin.html
    """
    user_form = access_pair_instance(request.form)

    if user_form.validate_on_submit():
        pairs = AccessPairs(
            access_code_id=user_form.access_code_id.data,
            space_number_id=user_form.space_number_id_fk.data,
        )
        db.session.add(pairs)
        db.session.commit()

        user_form.access_code_id.data = ""
        user_form.space_number_id_fk.data = ""
        flash("Space Assignment Added Successfully")

    return redirect(request.referrer)


@site.route("/post/approver/add", methods=["POST"])
@include_login_form
def add_approver():
    """
    Route used to add approvers to database, applied on admin.html
    """
    user_form = approver_instance(request.form)

    if user_form.validate_on_submit():
        approver = Approvers(
            approver_id=user_form.approver_id.data,
            role_approved_by=current_user.get_id(),
        )
        db.session.add(approver)
        db.session.commit()

        user_form.building_number.data = ""
        user_form.access_approver_id.data = ""
        flash("Space Approver Added Successfully")

    return redirect(request.referrer)


@site.route("/post/code/add", methods=["POST"])
@include_login_form
def add_code():
    """
    Route used to add approvers to database, applied on admin.html
    """
    user_form = access_code_form_instance(request.form)

    if user_form.validate_on_submit():
        code = AccessCodes(
            access_description=user_form.access_description.data,
            created_by=current_user.get_id(),
            authorized_by=user_form.authorized_by.data,
            # created_on is has a db default value
        )
        db.session.add(code)
        db.session.commit()

        user_form.access_description.data = ""
        user_form.authorized_by.data = ""
        flash("Access Code Added Successfully")

    return redirect(request.referrer)


@site.route("/post/request/add", methods=["POST"])
@include_login_form
def add_request():
    """
    Route used to make an order basket that uses session storage
    """
    user_form = request_form_instance(request.form)

    # logic for storing sessions
    session.modified = True

    if session.get("order"):
        pass
    else:
        session["order"] = []

    if user_form.validate_on_submit():
        floor_number = user_form.floor.data
        wing_number = user_form.wing.data
        room_number = user_form.room.data
        building_number = user_form.building_number.data
        approver_id = user_form.approver_id.data
        assignment_id = user_form.assignment_id.data

        space_id = f"B{str(building_number).zfill(2)}{str(wing_number).zfill(2)}{str(floor_number).zfill(2)}{str(room_number).zfill(2)}"

        # query for space owner name
        pi_name = (
            Users.query.with_entities(Users.first_name, Users.last_name)
            .filter(Users.user_id == assignment_id)
            .first()
        )
        # query for buiding approver
        approver_name = (
            Users.query.with_entities(Users.first_name, Users.last_name)
            .join(Approvers, Users.user_id == Approvers.user_id)
            .filter(Approvers.approver_id == approver_id)
            .first()
        )

        print(pi_name)
        new_key = {
            "space_id": space_id,
            "building_number": building_number,
            "wing_number": wing_number,
            "floor_number": floor_number,
            "room_number": room_number,
            "space_owner": f"{pi_name.first_name.title()} {pi_name.last_name.title()}",
            "building_approver": f"{approver_name.first_name.title()} {approver_name.last_name.title()}",
            "access_code": "TBD",
            "space_owner_id": assignment_id,
            "building_approver_id": approver_id,
        }

        session["order"].append(new_key)

        user_form.building_number.data = ""
        user_form.wing.data = ""
        user_form.floor.data = ""
        user_form.room.data = ""
        user_form.approver_id.data = ""
        user_form.assignment_id.data = ""
        flash("Key Added Successfully")

    return ("", 204)


@site.route("/post/basket/add", methods=["GET", "POST"])
@include_login_form
def submit_basket():
    """
    Route used to find access codes and update local variables and add data to database
    """

    # access data in basket and obtain the requested rooms
    order_entries = session["order"]
    room_list = [i["space_id"] for i in order_entries]
    deduped_requested_rooms = list(tuple(set(room_list)))

    # need to finish this route

    # print("Route room check: ", unique_rooms_list)

    # use combos.py function to get access code
    # it returns a list of access codes
    # each requested key should be updated with an access code
    # the requests should be just of the unique codes but a column should store the rooms
    # so the user understands how many keys are needed
    # a message should also be provided.

    # use /table/matrix/ as a template for getting the input to the find_codes function
    # filter by building
    # replace with:  list(AccessPairs.query.with_entities(AccessPairs.access_code_id, AccessPairs.space_number_id).all())

    ##########################################################################################
    # Update Table UX
    ##########################################################################################
    results = AccessPairs.query.all()
    data = []
    for result in results:
        data.append(
            {"access_code": result.access_code_id, "space_id": result.space_number_id}
        )

    # get unique access codes and retrieve all records related to those codes
    # format is in code:[rooms] format
    code_id = set([i["access_code"] for i in data])
    new_data = []
    for record in code_id:
        filtered_ids = filter(lambda x: x["access_code"] == record, data)
        rooms = tuple([i["space_id"] for i in filtered_ids])
        entry = {"id": record, "value": rooms}
        new_data.append(entry)

    # find existing codes that the user has in possession
    # note:  may want to also find keys in queue but not complete and handle them differently
    # add filter of approved not equal to false so rejected requests are not part of this list
    existing_rooms = list(
        Requests.query.with_entities(Requests.spaces_requested)
        .distinct()
        .filter(Requests.user_id == current_user.get_id())
        .filter(Requests.request_status_id.not_in((3, 8, 9, 10)))
    )

    existing_codes = list(
        Requests.query.with_entities(Requests.access_code_id)
        .distinct()
        .filter(Requests.user_id == current_user.get_id())
        .filter(Requests.request_status_id.not_in((3, 8, 9, 10)))
    )
    existing_codes = [r for r, in existing_codes]

    waiting_for_codes_rooms = list(
        Requests.query.with_entities(Requests.spaces_requested)
        .distinct()
        .filter(Requests.user_id == current_user.get_id())
        .filter(Requests.request_status_id == 10)
    )

    existing_rooms2 = list(
        AccessPairs.query.with_entities(AccessPairs.space_number_id).filter(
            AccessPairs.access_code_id.in_(existing_codes)
        )
    )

    print("existing_rooms: ", existing_rooms)
    print("existing_rooms2: ", existing_rooms2)

    existing_codes2 = list(
        Requests.query.with_entities(
            Requests.access_code_id, Requests.request_status_id
        )
        .distinct()
        .filter(Requests.user_id == current_user.get_id())
        .filter(Requests.request_status_id.not_in((3, 8, 9, 10)))
    )
    print("existing codes: ", existing_codes)
    print("existing codes2: ", existing_codes2)
    print("dedup: ", deduped_requested_rooms)
    # new requests and existing requests combined
    rooms_without_codes = [r for r, in waiting_for_codes_rooms]
    total_rooms = deduped_requested_rooms + existing_rooms2 + rooms_without_codes
    unique_rooms_flattened = tuple(
        set([i if type(i) is str else i[0] for i in total_rooms])
    )
    # returns dictionary of access codes and rooms found, list of access codes, and rooms without codes
    codes = find_codes(unique_rooms_flattened, new_data)
    print("calc codes", codes["access_codes"])
    #  Update session variable that updates order basket
    print("updating session variables and table")
    for record in order_entries:
        for i, code in enumerate(codes["access_codes"]):
            # print("test", record)
            if code != 0:
                # Assigns code to key request entry in the table
                # This replaces the default value of TBD with the appropriate code
                for room in codes["requested_spaces"][i][code]:
                    if record["space_id"] == room:
                        record["access_code"] = code
                        print(f"Request for room {room} will be code {code}")
            else:
                # TBD is the default value in the table and the replacement of this value
                # indicates the actions being taken since there is no existing code
                # note:  the if below is probably not needed
                if (record["access_code"] == "TBD") or (
                    record["access_code"] == "Request in Progress"
                ):
                    record["access_code"] = "Key Code Requested"
                    print(
                        f"Requested room not found in access matrix.  Requested new code to be generated."
                    )

    # logic for storing sessions
    # need to improve messaging based on case
    session.modified = True
    session["order"] = order_entries

    if int(codes["access_codes"][0]) != 0:
        msg = "Exact Match Found"
    else:
        msg = "Match Not Found"

    session["msgs"] = []
    session["msgs"].append(msg)

    ##################################################################################
    # Database Updates
    ##################################################################################
    # print("latest test: ", codes)
    # create list of the room codes returned and the existing codes already available to the user
    # room_codes = np.ravel([list(v.keys()) for v in codes["requested_spaces"]])
    room_numbers = []
    room_codes = []
    for i in codes["requested_spaces"]:
        room_codes = room_codes + list(i.keys())
        room_numbers = room_numbers + list(i.values())

    # rooms = [list(i.values())[0] for i in code["requested_spaces"]]
    # rooms_list = []
    # for i in rooms:
    #     rooms_list = rooms_list + i
    # print(rooms_list)

    # print("room codes found: ", room_codes)
    # print("existing rooms: ", existing_rooms)
    # print("existing codes: ", existing_codes)
    # print("key dictionary found: ", codes["requested_spaces"])
    # [1,2,'Request in Progress']
    for code in room_codes:
        if (code == "Key Code Requested") or (code == "Request in Progress"):
            # proceed to next iteration
            continue
        elif int(code) in [j[0] for j in existing_codes2]:
            print(f"code {code} previously requested and given, no action needed")
        else:
            print(f"requesting approval for code {code}")
            print(f"code_requestd_spaces: ", codes["requested_spaces"])
            # [{1: ('B24010101',)}, {2: ('B24020101', 'B24020102')}, {'Request in Progress': 'B24010201'}]
            print(f"order entries: ", order_entries)
            # [{'space_id': 'B24020101', 'building_number': 24, 'wing_number': 2, 'floor_number': 1, 'room_number': 1, 'space_owner': 'Will Wright', 'building_approver': 'Bob Turtle', 'access_code': 2, 'space_owner_id': 2, 'building_approver_id': 1}]
            # add to request table

            # need to fix this part - rerun using request for 'B24020102'
            for obj in codes["requested_spaces"]:
                for k, v in obj.items():
                    filter_record = [
                        (i["space_owner_id"], i["building_approver_id"])
                        for i in order_entries
                        if i["space_id"] in v
                    ]
                    print(v)
                    print(filter_record)

                    if len(filter_record) > 0:
                        new_request = Requests(
                            user_id=current_user.get_id(),
                            spaces_requested=", ".join(v),
                            building_number=v[0][1:3],
                            space_owner_id=filter_record[0][0],
                            approver_id=filter_record[0][1],
                            access_code_id=int(k),
                            request_status_id=1,
                        )
                        db.session.add(new_request)
                        db.session.commit()
                        print("request added to Requests table")
    # when an existing key is not returned in the room_codes to issue then that key should be returned

    for held_code in existing_codes2:
        user_id = current_user.get_id()
        code_id = held_code[0]
        print("code_id: ", code_id)
        print("room codes: ", room_codes)
        code_status = held_code[1]
        if str(code_id) not in room_codes:
            # update key record to be deleted if the request status is 1 (key submitted, but not yet approved (not in queue yet))
            if code_status in [1, 10]:
                print("Delete duplicate request that have not been approved")
                Requests.query.filter(Requests.user_id == user_id).filter(
                    Requests.access_code_id == code_id
                ).delete(synchronize_session=False)

                db.session.commit()

            # for request status 2,4, 5 (mid-request process), the request should be set to 8 *Key Returned) and inventory should be updated
            elif code_status in [2, 4, 5]:
                print(
                    'Update request for key not yet distributed to be "returned" to stop distribution'
                )
                Requests.query.filter(Requests.user_id == user_id).filter(
                    Requests.access_code_id == code_id
                ).update({"request_status_id": 8}, synchronize_session=False)

                db.session.commit()

            # update key status to show the key needs returned if the request status is 6 (key assigned)
            elif code_status == 6:
                print(
                    f"Update request to have key {held_code[0]} to be returned, place hold on existing orders"
                )
                # update the requests status and update the orders table
                Requests.query.filter(Requests.user_id == user_id).filter(
                    Requests.access_code_id == code_id
                ).update({"request_status_id": 7}, synchronize_session=False)

                db.session.commit()

            # no action needed for request status 3, 7, 8, 9, 10
            else:
                print(f"No existing records need changed for this request")

    # what happened to B24010201
    # check if keys requested are being requested again
    print("Prev room numbers requested without codes: ", rooms_without_codes)
    # may need to flatten room_numbers or make room_numbers be the flattened list of rooms that are returned - don't include missing codes
    print("Final rooom numbers requested: ", room_numbers)
    if len(rooms_without_codes) > 1:
        for room22 in rooms_without_codes:
            if room22 not in room_numbers:
                print(f"Deleting {room22} request from database")
                user_id = current_user.get_id()
                (
                    Requests.query.filter(Requests.user_id == user_id)
                    .filter(Requests.request_status_id == 10)
                    .filter(Requests.spaces_requested == room22)
                    .delete(synchronize_session=False)
                )

                db.session.commit()
    elif len(rooms_without_codes) == 1:
        room22 = rooms_without_codes[0]
        if room22 not in room_numbers:
            print(f"Deleting {room22} from database")
            user_id = current_user.get_id()
            (
                Requests.query.filter(Requests.user_id == user_id)
                .filter(Requests.request_status_id == 10)
                .filter(Requests.spaces_requested == room22)
                .delete(synchronize_session=False)
            )
    else:
        print("No code requests deletions needed")

        # if len(room_numbers) == 1:
        #     room33 = rooms_without_codes[0]
        #     print("inner loop: ", room33)
        #     user_id = current_user.get_id()
        #     (
        #         Requests.query.filter(Requests.user_id == user_id)
        #         .filter(Requests.access_code_id == 0)
        #         .filter(Requests.spaces_requested == room33)
        #         .delete(synchronize_session=False)
        #     )
        #     db.session.commit()
        # else:
        pass

    # loop through missing dictionary
    # add code to access_pairs
    if len(codes["missing"]) > 0:
        for i in codes["missing"]:
            # create new table for these requests
            print("Request for new code to be generated for these rooms: ", i)

            filtered_results = [
                (j["space_owner_id"], j["building_approver_id"])
                for j in order_entries
                if j["space_id"] == i
            ]
            if (len(filtered_results) > 0) and (
                i not in [j[0] for j in existing_codes2]
            ):
                new_request = Requests(
                    user_id=current_user.get_id(),
                    spaces_requested=i,
                    building_number=i[1:3],
                    space_owner_id=0,
                    approver_id=filtered_results[0][1],
                    access_code_id=0,
                    request_status_id=10,
                )
                db.session.add(new_request)
                db.session.commit()
            else:
                print("Missing room is already in requests - no action needed")
    else:
        print("No missing codes requested")

    return ("", 204)


@site.route("/post/basket/msg", methods=["GET", "POST"])
@include_login_form
def basket_msg():
    # print(msg)
    # logic for storing sessions
    # session.modified = True
    # if session.get("msgs"):
    #     pass
    # else:
    #     session["msgs"] = []

    # session["msgs"].append(msg)

    return render_template("dynamic/_msg.html")


# clear session data
@site.route("/post/basket/clear", methods=["GET"])
@include_login_form
def clear_session():
    # update webpage with variables
    # html = render_template("dynamic/_orders.html")
    # remove session variables
    print("Clearing Session Variable")
    for session_variable in ["order", "msgs"]:
        try:
            # logic for storing sessions
            session.modified = True
            session.pop(session_variable)
        except KeyError:
            print("Session Order does not exist or other error.")

    # return html
    return render_template("dynamic/_orders.html")


# -------------------------- SITE ACCESS -------------------------------------


@site.route("/login", methods=["GET", "POST"])
@site.route("/")
def login():
    """
    Login page and default page for app
    """

    if current_user.is_authenticated:
        return redirect(url_for("site.index"))

    username = None
    password = None
    passed_verification = None

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        form.username.data = ""
        form.password.data = ""

        find_username = Authentication.query.filter_by(username=username).first()
        if find_username:
            passed_verification = check_password_hash(
                find_username.password_hash, password
            )
            if passed_verification:
                login_user(find_username)
                flash("Login Successful")
                return redirect(url_for("site.index"))
            flash("Wrong Password - Try Again")
        else:
            flash("User Not Found - Try again")
    return render_template("login.html", form=form)


@site.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration page to create password
    Note:  Need to add temporary password
    """
    # on unsuccessful login the below page is loaded
    form = RegisterForm()

    username = None
    if form.validate_on_submit():
        user_registered = Users.query.filter_by(email=form.username.data).first()

        if user_registered is None:
            flash(
                f"Username {form.username.data} is not found.  Please try another email or request access from a building manager."
            )
            return render_template("register.html", form=form)

        username = Authentication.query.filter_by(username=form.username.data).first()

        if username is None:
            hashed_pw = generate_password_hash(form.password.data, "pbkdf2:sha256")
            username = Authentication(
                id=user_registered.user_id,
                username=form.username.data,
                password_hash=hashed_pw,
            )
            db.session.add(username)
            db.session.commit()
            flash("Password added successfully")
            username = form.username.data
        else:
            flash(f"User {form.username.data} already exists")
        form.username.data = ""
        form.password.data = ""
        form.password2.data = ""
    return render_template("register.html", form=form)


@site.route("/logout", methods=["GET", "POST"])
@include_login_form
@login_required
def logout():
    """
    Logout function
    """
    logout_user()
    flash("You are now logged out")
    return redirect(url_for("site.login"))
