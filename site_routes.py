from flask import Blueprint, render_template, jsonify, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from query import login_request
from models import db, Authentication
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create Form Class
class LoginForm(FlaskForm):
    '''
    Login Form fields
    '''
    username = StringField("Input your Username.", validators=[DataRequired()])
    password = StringField("Input your Password.", validators=[DataRequired()])
    submit = SubmitField('Submit')


# views to not include
login_form_views = []


def include_login_form(fn):
    login_form_views.append(fn.__name__)
    return fn


site = Blueprint('site', __name__)


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
                first_name='Erin',
                last_name='Wills',
                username=form.username.data,
                password_hash=form.password.data
            )
            db.session.add(user)
            db.session.commit()
        name = form.username.data
        form.username.data = ''
        form.password.data = ''
        flash("User Added Successfully")

    return {
        'name': name,
        'form': form
    }

@site.route('/')
@include_login_form
def index():
    return render_template('index.html')

@site.route('/login', methods=['GET', 'POST'])
@include_login_form
def test():
    return render_template('index.html')
