from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Authentication, Users
# from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, userform_instance


# allow for multiple route types, see also api_routes.py
site = Blueprint("site", __name__)


# ---------- WIDELY USED PAGE PARAMETERS ----------------------------


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
    return render_template("index.html")


@site.route("/users")
@include_login_form
def users_page():
    """
    User information page, currently holds add users form
    """

    user_form = userform_instance()

    return render_template("user.html", user_form=user_form)


# ---------- FORM ROUTES ----------------------------


# User Addition by Administrator
# maybe rename route /post/user/add
@site.route("/post/add_user", methods=["POST"])
@include_login_form
def add_user():
    """
    Route used to add users to database, applied on user.html
    """
    user_form = userform_instance(request.form)

    if user_form.validate_on_submit():
        name = Authentication.query.filter_by(username=user_form.username.data).first()

        if name is None:
            user = Users(
                first_name=user_form.first_name.data,
                last_name=user_form.last_name.data,
                title_id=user_form.title.data,
                role_id=user_form.role.data,
                email=user_form.email,
            )
            db.session.add(user)
            db.session.commit()

        user_form.first_name.data = ""
        user_form.last_name.data = ""
        user_form.title.data = ""
        user_form.role.data = ""
        flash("User Added Successfully")

    return redirect(request.referrer)


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
