from flask import json
from src.app import app
from src.github import get_user_info
from flask_pydantic import validate


@app.route("/", methods=["GET"])
def index():
    return f"Welcome to PyroMetric backend!"


@app.route("/generalFeedback", methods=["POST"])
def generalFeedback():
    return f"Placeholder to query the Gemini API"


def stream_event(event, data):
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@app.route("/score/<gh_username>", methods=["GET"])
@validate()
def score(gh_username: str):
    def generate():
        yield stream_event(
            "message", {"type": "metadata", "data": get_user_info(gh_username)}
        )
        yield stream_event("message", {"type": "impact", "data": {}})
        yield stream_event("message", {"type": "experience", "data": {}})
        yield stream_event("message", {"type": "quality", "data": {}})
        yield stream_event("message", {"type": "ability", "data": {}})
        yield stream_event("close", None)

    return app.response_class(generate(), mimetype="text/event-stream")
