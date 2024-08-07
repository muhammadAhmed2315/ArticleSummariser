from extensions import db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    generations = db.relationship("Generation", backref="author", lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Generation(db.Model):
    __tablename__ = "generations"

    id = db.Column(db.Integer, primary_key=True)
    time_generated = db.Column(db.DateTime)
    mode = db.Column(db.String)
    model = db.Column(db.String)
    inputText = db.Column(db.Text)
    outputText = db.Column(db.Text)
    aboutText = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(
        self, mode, model, time_generated, inputText, outputText, aboutText, user_id
    ):
        self.mode = mode
        self.model = model
        self.time_generated = time_generated
        self.inputText = inputText
        self.outputText = outputText
        self.aboutText = aboutText
        self.user_id = user_id
