from flask import Blueprint, request, redirect, render_template, flash
from models import db, Authentication, Users
import json
from query import login_request
from forms import LoginForm, CreateUserForm, CreateBuildingForm, CreateRoomForm


api = Blueprint("api", __name__, url_prefix="/api")

# ---------------------------------------------------------- #
# Universal routes
# ---------------------------------------------------------- #

# ---------------------------------------------------------- #


# User Addition by Administrator
@api.route("/post/add_user", methods=["POST"])
def add_user():
    user_form = CreateUserForm(request.form)

    # list of options
    title_list = [(1, "Option 1"), (2, "Option 2")]
    user_form.title.choices = title_list

    role_list = [(1, "General user"), (2, "Admin")]
    user_form.role.choices = role_list

    if user_form.validate_on_submit():
        # name = Authentication.query.filter_by(username=form.username.data).first()
        name = None
        if name is None:
            user = Users(
                first_name=user_form.first_name.data,
                last_name=user_form.last_name.data,
                title_id=user_form.title.data,
                role_id=user_form.role.data,
            )

            db.session.add(user)
            db.session.commit()

        user_form.first_name.data = ""
        user_form.last_name.data = ""
        user_form.title.data = ""
        user_form.role.data = ""
        flash("User Added Successfully")

    return render_template("user.html", user_form=user_form)


# Login routes
@api.route("/login")
def login():
    """
    Used in modal js
    """
    # db.create_all(bind=['login'])

    name = Authentication.query.order_by(Authentication.login_id.desc()).first()
    return json.dumps({"username": name.username, "password": name.password_hash})


@api.route("/modalsubmit", methods=["POST"])
def submit_login():
    """
    Login
    """
    username = request.form["user"]
    password = request.form["password"]

    print(f"Username is {username}")
    print(f"Password is {password}")

    # db.create_all(bind=['login'])

    add_credentials = Authentication(
        first_name="Erin33", last_name="Wills33", username=username, password=password
    )

    db.session.add(add_credentials)
    db.session.commit()

    return redirect(request.referrer)


# ---------------------------------------------------------- #
# Unit page routes


@api.route("/submission")
def submission():
    """
    Submission api
    """
    data = login_request()
    return json.dumps(data)
