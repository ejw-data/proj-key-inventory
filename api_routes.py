from flask import Blueprint, request, redirect, render_template, flash
from models import db, Authentication, Users
import json
from forms import LoginForm, CreateUserForm, CreateBuildingForm, CreateRoomForm


api = Blueprint("api", __name__, url_prefix="/api")

# ---------------------------------------------------------- #
# Universal routes
# ---------------------------------------------------------- #

# API routes

