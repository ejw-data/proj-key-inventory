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

# # Login routes
# @api.route("/login")
# def login():
#     """
#     Used in modal js
#     """
#     # db.create_all(bind=['login'])

#     name = Authentication.query.order_by(Authentication.login_id.desc()).first()
#     return json.dumps({"username": name.username, "password": name.password_hash})


# @api.route("/modalsubmit", methods=["POST"])
# def submit_login():
#     """
#     Login
#     """
#     username = request.form["user"]
#     password = request.form["password"]

#     print(f"Username is {username}")
#     print(f"Password is {password}")

#     # db.create_all(bind=['login'])

#     add_credentials = Authentication(
#         first_name="Erin33", last_name="Wills33", username=username, password=password
#     )

#     db.session.add(add_credentials)
#     db.session.commit()

#     return redirect(request.referrer)


# ---------------------------------------------------------- #
# Unit page routes


# @api.route("/submission")
# def submission():
#     """
#     Submission api
#     """
#     data = login_request()
#     return json.dumps(data)
