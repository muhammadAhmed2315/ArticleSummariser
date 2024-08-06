from flask import request, Blueprint, jsonify, render_template
from openai import OpenAI

summariser = Blueprint("summariser", __name__)
client = OpenAI()


@summariser.route("/summarise")
def summarise():
    return render_template("summariser.html")


@summariser.route("/summarise_text", methods=["get", "post"])
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

    def generate():
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

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content)
                yield (chunk.choices[0].delta.content)

    return generate(), {"Content-Type": "text/plain"}
