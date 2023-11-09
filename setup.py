from flask import Flask
from db_paths import path
from config import secret_key


def create_app():
    '''
    Initiate Flask
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key

    ENV = 'dev'

    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = path["key_inventory"]
        app.config['SQLALCHEMY_BINDS'] = {
            'key_inventory':    path["key_inventory"]
        }
    elif ENV == 'prod':
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'webaddress'
        app.config['SQLALCHEMY_BINDS'] = {
            'login':    'sqlite:///login-flask.db',
            'utility':  'sqlite:///utility.db'
        }
    else:
        print("Please select an environment:  developement or production.")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app
