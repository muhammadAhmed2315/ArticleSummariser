import logging
from flask import Flask, session
from flask_migrate import Migrate
from extensions import db, login_manager
from models import User

# Configure logging
log = logging.getLogger("werkzeug")
log.disabled = True

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"

# Initialize database
db.init_app(app)
Migrate(app, db)

# Initialize login manager
login_manager.init_app(app)
login_manager.login_view = "user_authentication.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Create database tables
with app.app_context():
    db.create_all()

# Register blueprints and run app (only if this file is run directly)
if __name__ == "__main__":
    # Import blueprints
    from summariser.app import summariser
    from login.app import user_authentication
    from history.app import user_history

    # Register blueprints
    app.register_blueprint(user_authentication)
    app.register_blueprint(summariser)
    app.register_blueprint(user_history)

    # Run the app
    app.run(debug=True)
