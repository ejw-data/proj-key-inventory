from flask import Flask
from db_paths import path
import os

secret_key = os.environ.get("KEY_SECRET")

def create_app():
    """
    Initiate Flask
    """
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SECRET_KEY"] = secret_key

    ENV = "dev"

    if ENV == "dev":
        app.debug = True
        app.config["SQLALCHEMY_DATABASE_URI"] = path["local_db"]
        app.config["SQLALCHEMY_BINDS"] = {"key_inventory": path["local_db"]}
    elif ENV == "prod":
        app.debug = False
        app.config["SQLALCHEMY_DATABASE_URI"] = path["gcp_db"]
        app.config["SQLALCHEMY_BINDS"] = {"key_inventory": path["gcp_db"]}
    else:
        print("Please select an environment:  developement or production.")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app
