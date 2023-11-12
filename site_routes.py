from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from query import login_request
from models import db, Authentication, Users
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import LoginForm, CreateUserForm, RegisterForm, userform_instance
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)

site = Blueprint("site", __name__)


# --------------- Send parameters to
# views to not include
login_form_views = []


# "site." is needed becasue using blueprints
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
    name = user_record.first_name.title()
    form = LoginForm()

    # if form.validate_on_submit():
    #     name = Authentication.query.filter_by(username=form.username.data).first()
    #     if name is None:
    #         user = Authentication(
    #             id=name,
    #             username=form.username.data,
    #             password_hash=form.password.data,
    #         )
    #         db.session.add(user)
    #         db.session.commit()
    #     name = form.username.data
    #     form.username.data = ""
    #     form.password.data = ""
    #     flash("User Added Successfully")

    return {"name": name, "form": form}


@site.route("/")
# @login_required
@include_login_form
def index():
    """
    In future this will be the login page
    """
    return render_template("index.html")


# -------------------------- USERS ---------------------------------------------
@site.route("/users")
@include_login_form
def users_page():
    """
    Administrator
    """

    user_form = userform_instance()

    return render_template("user.html", user_form=user_form)


# User Addition by Administrator
# maybe rename route /post/user/add
@site.route("/post/add_user", methods=["POST"])
@include_login_form
def add_user():
    user_form = userform_instance(request.form)

    if user_form.validate_on_submit():
        # name = Authentication.query.filter_by(username=form.username.data).first()
        name = None
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


# -------------------------- USERS ---------------------------------------------


@site.route("/login", methods=["GET", "POST"])
def login():
    """
    This will be merged with home route
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
    This will be merged with home route
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
    logout_user()
    flash("You are now logged out")
    return redirect(url_for("site.login"))
