from flask import json
from pydantic import BaseModel
from src.app import app
from src.github import get_user_info
from flask_pydantic import validate
import time


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
        time.sleep(0.5)  # simulate delay
        impact_data = {
            "score": 43,
            "feedback": [
                "You have lots of GitHub stars!",
                "You have a good amount of followers!",
            ],
        }
        yield stream_event("message", {"type": "impact", "data": impact_data})
        time.sleep(0.2)  # simulate delay
        experience_data = {
            "score": 80,
            "feedback": [
                "You have a good amount of experience in Python",
                "You have a good amount of experience in Java",
            ],
        }
        yield stream_event("message", {"type": "experience", "data": experience_data})
        time.sleep(0.3)  # simulate delay
        quality_data = {
            "score": 21,
            "feedback": [],
        }
        yield stream_event("message", {"type": "quality", "data": quality_data})
        ability_data = {
            "score": 100,
            "feedback": ["Wow! You are a great developer!"],
        }
        yield stream_event("message", {"type": "ability", "data": ability_data})
        yield stream_event("close", None)

    return app.response_class(generate(), mimetype="text/event-stream")


@app.route("/compare/<usernames_str>", methods=["GET"])
def score_only(usernames_str: str):
    usernames = usernames_str.split(",")
    time.sleep(1)  # simulate delay
    return [{}]
