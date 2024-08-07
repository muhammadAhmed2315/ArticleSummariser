from flask import render_template, redirect, request, url_for, Blueprint, flash, jsonify
from flask_login import login_user, login_required, logout_user
from models import User
from extensions import db
import math
from flask_login import current_user

ITEMS_PER_PAGE = 5


user_history = Blueprint("user_history", __name__)


@user_history.route("/view_past_generations", methods=["get", "post"])
@login_required
def view_past_generations():
    return render_template("history.html")


@user_history.route("/get_past_generations/<int:page_number>", methods=["get", "post"])
def get_past_generations(page_number):
    user_generations = User.query.get(current_user.get_id()).generations
    user_generations = user_generations[::-1]
    max_pages = math.ceil(len(user_generations) // ITEMS_PER_PAGE)

    # Convert data into a dictionary
    user_generations = user_generations[
        (page_number - 1) * ITEMS_PER_PAGE : page_number * ITEMS_PER_PAGE
    ]

    for i, value in enumerate(user_generations):
        user_generations[i] = {
            "mode": value.mode,
            "model": value.model,
            "time_generated": value.time_generated,
            "inputText": value.inputText,
            "outputText": value.outputText,
            "aboutText": value.aboutText,
        }

    return jsonify({"data": user_generations, "max_pages": max_pages})
