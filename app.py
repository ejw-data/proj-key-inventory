from sqlalchemy_utils import database_exists
from site_routes import site
from api_routes import api
from setup import create_app
from models import db
from db_paths import path


app = create_app()
app.register_blueprint(api)
app.register_blueprint(site)
app.app_context().push()

db.init_app(app)

# generate database if it doesn't exist
if ~(database_exists(path["key_inventory"])):
    db.create_all(bind_key=['key_inventory'])


if __name__ == '__main__':
    app.run(debug=True)
