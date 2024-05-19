from flask import json, request
from pydantic import BaseModel
from src.app import app
from src.github import get_user_info, get_user_top_languages, get_repo_list, filter_repos_by_languages, get_files_to_scrape, retrieve_files
from src.routes.AIScorer import AIScorer
from flask_pydantic import validate
import time


@app.route("/", methods=["GET"])
def index():
    return f"Welcome to PyroMetric backend!"


@app.route("/feedback", methods=["POST"])
def feedback():
    link = request.json['link']
    languages = request.json['languages']
    
    # String splits github address and gets username
    username = link.split("/")[-1]
    
    repos = get_repo_list(username)
    language_repo_dict = filter_repos_by_languages(username, repos, languages, limit=1)
    files = get_files_to_scrape(username, language_repo_dict)
    file_content = retrieve_files(username, files)
    scorer = AIScorer()
    stringifiedFiles = scorer.getStringifiedFiles(file_content)
    feedback = scorer.getFeedback(stringifiedFiles)
    
    return feedback


def stream_event(event, data):
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@app.route("/score/<gh_username>", methods=["GET"])
@validate()
def score(gh_username: str):
    def generate():
        yield stream_event(
            "message", {"type": "metadata", "data": get_user_info(gh_username)}
        )
        yield stream_event(
            "message",
            {"type": "languages", "data": get_user_top_languages(gh_username)},
        )
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
def compare(usernames_str: str):
    usernames = usernames_str.split(",")
    if len(usernames) > 30:
        return "Max 30 usernames", 400

    user_data = [get_user_info(username) for username in usernames]
    time.sleep(1)  # simulate delay

    response = [{"user_data": user_data[i]} for i in range(len(user_data))]

    return response
