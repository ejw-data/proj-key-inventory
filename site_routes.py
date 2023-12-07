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
    # KeyInventory,
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
                email=user_form.email.data,
            )
            db.session.add(user)
            db.session.commit()

            user_form.first_name.data = ""
            user_form.last_name.data = ""
            user_form.title_fk.data = ""
            user_form.role.data = ""
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
    Route used to add buildings to database, applied on admin.html
    """
    user_form = request_form_instance(request.form)

    # logic for storing sessions
    session.modified = True

    if session.get('order'):
        pass
    else:
        session['order'] = []

    # # I will need to clear the session on submit
    # session.clear()

    if user_form.validate_on_submit():
        floor_number = user_form.floor.data
        wing_number = user_form.wing.data
        room_number = user_form.room.data
        building_number = user_form.building_number.data
        # room_list = ["B24010101"]
        # code = get_access_code(room_list)[0]
        space_id = f"B{str(building_number).zfill(2)}{str(floor_number).zfill(2)}{str(wing_number).zfill(2)}{str(room_number).zfill(2)}"

        new_key = {
            'space_id': space_id,
            'building_number': building_number,
            'wing_number': wing_number,
            'floor_number': floor_number,
            'room_number': room_number,
            'space_owner': "Ted",
            'building_approver': "Joe"
        }

        session['order'].append(new_key)

        user_form.building_number.data = ""
        user_form.wing.data = ""
        user_form.floor.data = ""
        user_form.room.data = ""
        user_form.approver_id.data = ""
        flash("Key Added Successfully")

    return ('', 204)


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
