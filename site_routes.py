from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from query import login_request
from models import db, Authentication, Users
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import LoginForm, CreateUserForm, userform_instance


# views to not include
login_form_views = []


def include_login_form(fn):
    login_form_views.append(fn.__name__)
    return fn


site = Blueprint("site", __name__)


@site.context_processor
def additional_parameters():
    if request.endpoint in login_form_views:
        return {}

    name = None
    form = LoginForm()

    if form.validate_on_submit():
        name = Authentication.query.filter_by(username=form.username.data).first()
        if name is None:
            user = Authentication(
                first_name="Erin",
                last_name="Wills",
                username=form.username.data,
                password_hash=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
        name = form.username.data
        form.username.data = ""
        form.password.data = ""
        flash("User Added Successfully")

    return {"name": name, "form": form}


@site.route("/")
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
@include_login_form
def login():
    """
    This will be merged with home route
    """
    # on a successful login the index page is loaded
    return redirect(url_for("index"))

    # on unsuccessful login the below page is loaded
    return render_template("login.html")


@site.route("/logout", methods=["GET", "POST"])
@include_login_form
# @login_required
def logout():
    return redirect(url_for("site.users_page"))
