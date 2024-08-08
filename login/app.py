from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from .forms import LoginForm, RegisterForm
from extensions import db
from validate_email_address import validate_email


user_authentication = Blueprint("user_authentication", __name__)


@user_authentication.route("/")
def home():
    return render_template("home.html")


@user_authentication.route("/logout")
def logout():
    logout_user()
    return render_template("home.html")


@user_authentication.route("/login", methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("summariser.summarise"))

    loginForm = LoginForm()

    if loginForm.is_submitted() and loginForm.validate():
        # if email has incorrect format
        if not validate_email(loginForm.email.data):
            loginForm.email.errors.append("Email is invalid")
            return render_template("login.html", loginForm=loginForm)

        # if email not registered or password incorrect
        user = User.query.filter_by(email=loginForm.email.data).first()
        if not user or (user and not user.check_password(loginForm.password.data)):
            loginForm.password.errors.append("Incorrect email or password")
            return render_template("login.html", loginForm=loginForm)

        # else login user
        login_user(user)

        next = request.args.get("next")

        if next == None or next[0] != "/":
            next = url_for("summariser.summarise")

            return redirect(next)

    return render_template("login.html", loginForm=loginForm)


@user_authentication.route("/register", methods=["get", "post"])
def register():
    registerForm = RegisterForm()

    if registerForm.is_submitted() and registerForm.validate():
        # Check if valid email
        if not validate_email(registerForm.email.data):
            registerForm.email.errors.append("Email is invalid")
            return render_template("register.html", registerForm=registerForm)

        # Check if email already registered
        user = User.query.filter_by(email=registerForm.email.data).first()
        if user:
            registerForm.email.errors.append(
                "You have already registered with this email address."
            )
            return render_template("register.html", registerForm=registerForm)

        # Check if passwords match
        if registerForm.password.data != registerForm.pass_confirm.data:
            registerForm.password.errors.append("Password and confirmation don't match")
            registerForm.pass_confirm.errors.append(
                "Password and confirmation don't match"
            )
            return render_template("register.html", registerForm=registerForm)

        else:
            user = User(registerForm.email.data, registerForm.password.data)
            db.session.add(user)
            db.session.commit()
            # login_user(user)
            return redirect(url_for("user_authentication.home"))

    return render_template("register.html", registerForm=registerForm)
