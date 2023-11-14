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

    __bind_key__ = "key_inventory"
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(25))


class Approvers(db.Model):
    """
    Approvers
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "access_approvers"
    access_approver_id = db.Column(db.Integer, primary_key=True)
    approver_id = db.Column(db.Integer)
    role_approved_by = db.Column(db.String(128))
    date_approved = db.Column(db.Date)
    date_removed = db.Column(db.Date)


class Buildings(db.Model):
    """
    Building Info
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "buildings"
    building_number = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(128))
    building_description = db.Column(db.String(128))


class Rooms(db.Model):
    """
    Room Info
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "rooms"
    space_number_id = db.Column(db.String(128), primary_key=True)
    buidlding_number = db.Column(db.Integer)
    floor_number = db.Column(db.Integer)
    wing_number = db.Column(db.Integer)
    room_number = db.Column(db.Integer)
    room_type = db.Column(db.Integer)


class RoomClassification(db.Model):
    """
    Room Classification
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "room_classification"
    room_type_id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(128))


class RoomAmenities(db.Model):
    """
    Room Info
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "room_amentities"
    space_number_id = db.Column(db.Integer, primary_key=True)
    room_projector = db.Column(db.Boolean)
    room_seating = db.Column(db.Integer)


class Requests(db.Model):
    """
    Key Requests
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "requests"
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    space_number_id = db.Column(db.String(128))
    building_number = db.Column(db.Integer)
    access_approver_id = db.Column(db.Integer)
    access_code_id = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    request_date = db.Column(db.Date)
    approved_date = db.Column(db.Date)
    approved = db.Column(db.Boolean)
    approval_comment = db.Column(db.String(128))
    rejection_comment = db.Column(db.String(128))


class KeysCreated(db.Model):
    """
    Keys fabricated
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "keys_created"
    key_number = db.Column(db.Integer, primary_key=True)
    key_copy = db.Column(db.Integer)
    access_code_id = db.Column(db.Integer)
    fabrication_status_id = db.Column(db.Integer)


class KeyStatus(db.Model):
    """
    Key availability
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "key_status"
    key_status_id = db.Column(db.Integer, primary_key=True)
    key_status = db.Column(db.String(128))


class KeyOrders(db.Model):
    """
    Approved keys being produced by key shop
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "key_orders"
    transaction_id = db.Column(db.Integer, primary_key=True)
    access_code_id = db.Column(db.Integer)


class KeyInventory(db.Model):
    """
    Key location
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "key_inventory"
    transaction_id = db.Column(db.Integer, primary_key=True)
    key_number = db.Column(db.Integer)
    key_copy = db.Column(db.Integer)
    date_transferred = db.Column(db.Date)
    date_returned = db.Column(db.Date)


class FabricationStatus(db.Model):
    """
    Status of Key being made
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "fabrication_status"
    fabrication_status_id = db.Column(db.Integer, primary_key=True)
    fabrication_status = db.Column(db.String(128))


class ApproverZones(db.Model):
    """
    Approvers responsible for spaces
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "approver_zones"
    building_number = db.Column(db.Integer, primary_key=True)
    access_approver_id = db.Column(db.Integer)


class ApprovalStatus(db.Model):
    """
    Status of key request from request to handoff
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "approval_status"
    status_code = db.Column(db.Integer, primary_key=True)
    status_code_name = db.Column(db.String(128))


class AccessPairs(db.Model):
    """
    Access codes for specific doors
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "access_pairs"
    access_code_id = db.Column(db.Integer, primary_key=True)
    space_number_id = db.Column(db.Integer, primary_key=True)


class AccessCodes(db.Model):
    """
    Specific codes
    """
    __bind_key__ = "key_inventory"
    __tablename__ = "access_codes"
    access_code_id = db.Column(db.Integer, primary_key=True)
    access_description = db.Column(db.String(128))
    created_by = db.Column(db.String(128))
    authorized_by = db.Column(db.Date)
    created_on = db.Column(db.Date)
