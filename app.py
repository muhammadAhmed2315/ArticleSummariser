from flask import Flask
from flask_migrate import Migrate
from extensions import db, login_manager
from summariser.app import summariser

import logging

log = logging.getLogger("werkzeug")
# log.disabled = True

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"

db.init_app(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = "user_authentication.login"

from login.app import user_authentication

app.register_blueprint(user_authentication)
app.register_blueprint(summariser)

# Create tables if they don't exist, within the application context
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
