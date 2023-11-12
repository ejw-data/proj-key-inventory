from flask_sqlalchemy import SQLAlchemy

# I can probably remove these part of the code - used in site_routes.py
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

db = SQLAlchemy()


class Authentication(db.Model, UserMixin):
    """
    App login
    need just user_id linked to Users and username and password_hash
    Note:  Naming of 'id' matters because only 'id' is accepted by flask_login login_user()
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "authentication"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Users(db.Model):
    """
    User Table
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    title_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    email = db.Column(db.String(25))


class Titles(db.Model):
    """
    Title table
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "titles"
    title_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))


class Roles(db.Model):
    """
    Role table
    """

    __bind_key = "key_inventory"
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(25))


#     # Column types
#     db.Column(db.Integer)
#     db.Column(db.String(25))
#     db.Column(db.Date)
#     db.Column(db.Float)
