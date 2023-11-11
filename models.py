from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Authentication(db.Model):
    """
    App login
    """

    __bind_key__ = "key_inventory"
    __tablename__ = "authentication"
    login_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    username = db.Column(db.String(25))
    password_hash = db.Column(db.String(25))

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


# class Organizations(db.Model):
#     '''
#     App login
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "organizations"
#     org_id = db.Column(db.Integer, primary_key=True)
#     org_name = db.Column(db.String(25))
#     contact_first_name = db.Column(db.String(25))
#     contact_last_name = db.Column(db.String(25))
#     contact_phone = db.Column(db.String(25))


# class Customers(db.Model):
#     '''
#     App login
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "customers"
#     cust_id = db.Column(db.Integer, primary_key=True)
#     org_id = db.Column(db.Integer)
#     status = db.Column(db.String(25))


# class Subscriptions(db.Model):
#     '''
#     App subscribers
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "subscriptions"
#     sub_id = db.Column(db.Integer, primary_key=True)
#     cust_id = db.Column(db.Integer)
#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)


# class Users(db.Model):
#     '''
#     App users
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "users"
#     user_id = db.Column(db.Integer, primary_key=True)
#     sub_id = db.Column(db.Integer)
#     account_type = db.Column(db.String)


# class Billing(db.Model):
#     '''
#     Customer billing
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "billing"
#     bill_id = db.Column(db.Integer, primary_key=True)
#     bill_address_1 = db.Column(db.String)
#     bill_address_2 = db.Column(db.String)
#     bill_city = db.Column(db.String)
#     bill_state = db.Column(db.String)
#     bill_zipcode = db.Column(db.String)
#     bill_frequency = db.Column(db.String)


# class Invoices(db.Model):
#     '''
#     Customer invoicing
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "invoices"
#     invoice_id = db.Column(db.Integer, primary_key=True)
#     bill_id = db.Column(db.Integer)
#     sub_id = db.Column(db.Integer)
#     price = db.Column(db.Float)
#     date_billed = db.Column(db.Date)
#     period_start = db.Column(db.Date)
#     period_end = db.Column(db.Date)


# class Receivables(db.Model):
#     '''
#     Payments
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "receivables"
#     receive_id = db.Column(db.Integer, primary_key=True)
#     invoice_id = db.Column(db.Integer)
#     amount_paid = db.Column(db.Float)
#     payment_type = db.Column(db.String)


# class Hosts(db.Model):
#     '''
#     Hosts
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "hosts"
#     host_id = db.Column(db.Integer, primary_key=True)
#     sub_id = db.Column(db.Integer)
#     host_first_name = db.Column(db.String)
#     host_last_name = db.Column(db.String)
#     host_email = db.Column(db.String)
#     host_phone = db.Column(db.String)
#     host_permission_group = db.Column(db.String)


# class Appointments(db.Model):
#     '''
#     Appointments
#     '''
#     __bind_key__ = "scheduler"
#     __tablename__ = "appointments"
#     event_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     host_id = db.Column(db.Integer)
