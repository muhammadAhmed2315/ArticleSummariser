from flask import request, Blueprint, render_template
from openai import OpenAI
from flask_login import login_required
from models import Generation
from datetime import datetime, timezone
from extensions import db
from flask_login import current_user
from app import app

summariser = Blueprint("summariser", __name__)
client = OpenAI()


@summariser.route("/summarise")
@login_required
def summarise():
    return render_template("summariser.html")


@summariser.route("/summarise_text", methods=["get", "post"])
@login_required
def summarise_text():
    data = request.get_json()
    inputText = data["message"]
    selectedMode = data["mode"]
    selectedModel = data["model"]

    system_prompt = {
        "summarise": "You are a concise summarizer. Focus on reducing the text to its "
        + "essential points, maintaining the main themes, conclusions, and significant "
        + "details without deviating from the original intent of the text.",
        "keyinfo": "You are designed to extract key information. Analyze the text to "
        + "identify and highlight the most crucial facts, figures, and details. Pay "
        + "particular attention to names, dates, locations, statistics, and specific "
        + "contributions or findings.",
        "entityrecognition": "You are an entity recognizer. Your task is to identify "
        + "and list all entities such as people, places, organizations, dates, and other "
        + "proper nouns present in the text. Provide these entities in a structured and "
        + "categorized format if possible.",
    }
    content_prompt_prefix = {
        "summarise": "Here is the text I need summarized: ",
        "keyinfo": "Extract the key information from this text: ",
        "entityrecognition": "I need all the entities recognized in the following text: ",
    }

    def generate(user_id):
        stream = client.chat.completions.create(
            model=selectedModel,
            messages=[
                {"role": "system", "content": system_prompt[selectedMode]},
                {
                    "role": "user",
                    "content": content_prompt_prefix[selectedMode] + inputText,
                },
            ],
            stream=True,
        )

        output = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                output += chunk.choices[0].delta.content
                yield (chunk.choices[0].delta.content)

        # Update the database
        generation = Generation(
            selectedMode,
            selectedModel,
            datetime.now(timezone.utc),
            inputText,
            output,
            user_id,
        )
        with app.app_context():
            db.session.add(generation)
            db.session.commit()

    return generate(current_user.get_id()), {"Content-Type": "text/plain"}
