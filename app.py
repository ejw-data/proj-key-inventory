from sqlalchemy_utils import database_exists
from site_routes import site
from api_routes import api
from setup import create_app
from models import db
from db_paths import path
from models import Authentication
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)

app = create_app()
app.register_blueprint(api)
app.register_blueprint(site)
app.app_context().push()

db.init_app(app)

# flask_login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(login_id):
    return Authentication.query.get(int(login_id))



# generate database if it doesn't exist
if ~(database_exists(path["key_inventory"])):
    db.create_all(bind_key=["key_inventory"])


if __name__ == "__main__":
    app.run(debug=True)
