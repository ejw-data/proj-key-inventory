from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# I can probably remove these part of the code - used in site_routes.py
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

db = SQLAlchemy()

# # create view
# class AccessGridView(db.Model):
#     """
#     A PostgreSQL view that shows all the rooms available in each access code
#     """
#     __bind_key__ = "key_inventory"
#     __tablename__ = 'temp_matrix'
#     access_code_id = db.Column(db.String(10))
#     b24010101 = db.Column(db.Integer)
#     b24020101 = db.Column(db.Integer)
#     b24020102 = db.Column(db.Integer)


class Approvers(db.Model):
    """
    Approvers
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "approvers"
    approver_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    role_approved_by = db.Column(db.Integer)
    date_approved = db.Column(db.Date, server_default=func.now())
    date_removed = db.Column(db.Date)


# this is somewhat of an odd table that maybe can be merged into another table??
class AccessCodes(db.Model):
    """
    Specific codes
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "access_codes"
    access_code_id = db.Column(db.Integer, primary_key=True)
    access_description = db.Column(db.String(128))
    created_by = db.Column(db.Integer)
    authorized_by = db.Column(db.Integer)
    created_on = db.Column(db.Date, server_default=func.now())


class AccessPairs(db.Model):
    """
    Access codes for specific doors
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "access_pairs"
    access_code_id = db.Column(db.Integer, primary_key=True)
    space_number_id = db.Column(db.Integer, primary_key=True)


class RequestStatus(db.Model):
    """
    Status of key request from request to handoff
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "request_status"
    request_status_id = db.Column(db.Integer, primary_key=True)
    request_status_name = db.Column(db.String(128))


class Zones(db.Model):
    """
    Approvers responsible for spaces
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "zones"
    building_number = db.Column(db.Integer, primary_key=True)
    approver_id = db.Column(db.Integer)


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


class Buildings(db.Model):
    """
    Building Info
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "buildings"
    building_number = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(128))
    building_description = db.Column(db.String(128))


class FabricationStatus(db.Model):
    """
    Status of Key being made
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "fabrication_status"
    fabrication_status_id = db.Column(db.Integer, primary_key=True)
    fabrication_status = db.Column(db.String(128))


# Key Inventory table is populated by trigger in postgreSQL DB
# Only a status column nd an in_use column needs updated manually.
class KeyInventory(db.Model):
    """
    Key location
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "key_inventory"
    request_id = db.Column(db.Integer, primary_key=True)
    key_copy = db.Column(db.Integer)
    access_code_id = db.Column(db.Integer)
    key_status_id = db.Column(db.Integer)
    date_transferred = db.Column(db.Date)
    date_returned = db.Column(db.Date)


class OrderStatus(db.Model):
    """
    Order status options
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "order_status"
    order_status_id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(128))


# Key Orders Table is populated by trigger in postgreSQL DB
# add a status column that is updated by the admin office
class KeyOrders(db.Model):
    """
    Approved keys being produced by key shop
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "key_orders"
    request_id = db.Column(db.Integer, primary_key=True)
    access_code_id = db.Column(db.Integer)
    order_status_id = db.Column(db.Integer)
    date_key_received = db.Column(db.Date)
    date_key_handoff = db.Column(db.Date)
    key_admin_user_id = db.Column(db.Integer)
    key_pickup_user_id = db.Column(db.Integer)
    hold_on_conditions = db.Column(db.Boolean)


class KeyStatus(db.Model):
    """
    Key availability
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "key_status"
    key_status_id = db.Column(db.Integer, primary_key=True)
    key_status = db.Column(db.String(128))


# should this have two primary keys
class KeysCreated(db.Model):
    """
    Keys fabricated
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "keys_created"
    request_id = db.Column(db.Integer, primary_key=True)
    key_copy = db.Column(db.Integer)
    access_code_id = db.Column(db.Integer)
    fabrication_status_id = db.Column(db.Integer)
    key_maker_user_id = db.Column(db.Integer)
    date_created = db.Column(db.Date)


# change approved to Integer where it can be "Request Approved", "Waiting Approval", "Request Rejected"
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
    approver_id = db.Column(db.Integer)
    access_code_id = db.Column(db.Integer)
    request_status_id = db.Column(db.Integer)
    request_date = db.Column(db.DateTime, server_default=func.now())
    approved_date = db.Column(db.Date)
    approved = db.Column(db.Boolean)
    approval_comment = db.Column(db.String(128))
    rejection_comment = db.Column(db.String(128))


class Roles(db.Model):
    """
    Role table
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(25))


class RoomAmenities(db.Model):
    """
    Room Info
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "room_amenities"
    space_number_id = db.Column(db.String(128), primary_key=True)
    room_projector = db.Column(db.Boolean)
    room_seating = db.Column(db.Integer)


class RoomClassification(db.Model):
    """
    Room Classification
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "room_classification"
    room_type_id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(128))


class Rooms(db.Model):
    """
    Room Info
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "rooms"
    space_number_id = db.Column(db.String(128), primary_key=True)
    building_number = db.Column(db.Integer)
    wing_number = db.Column(db.String(20))
    floor_number = db.Column(db.Integer)
    room_number = db.Column(db.Integer)
    room_type_id = db.Column(db.Integer)


class Titles(db.Model):
    """
    Title table
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "titles"
    title_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))


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
