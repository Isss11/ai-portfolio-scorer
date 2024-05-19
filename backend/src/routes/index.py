from flask import json, make_response
from src.app import app
from src.github import (
    get_user_info,
    get_user_top_languages,
    get_user_popularity,
    get_user_exerience,
    get_user_quality,
)
from flask_pydantic import validate


@app.route("/", methods=["GET"])
def index():
    return f"Welcome to PyroMetric backend!"


def stream_event(event, data):
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@app.route("/score/<gh_username>", methods=["GET"])
@validate()
def score(gh_username: str):
    def generate():
        yield stream_event(
            "message", {"type": "metadata", "data": get_user_info(gh_username)}
        )
        top_languages = get_user_top_languages(gh_username)[:3]
        yield stream_event(
            "message",
            {"type": "languages", "data": top_languages},
        )
        popularity = get_user_popularity(gh_username)
        yield stream_event("message", {"type": "impact", "data": popularity})
        user_experience = get_user_exerience(gh_username)
        yield stream_event("message", {"type": "experience", "data": user_experience})
        quality = get_user_quality(gh_username)
        yield stream_event("message", {"type": "quality", "data": quality})
        overall_data = {
            "score": int(
                (popularity["score"] + user_experience["score"] + quality["score"]) / 3
            ),
            "feedback": [],
        }
        yield stream_event("message", {"type": "overall", "data": overall_data})
        yield stream_event("close", None)

    return app.response_class(generate(), mimetype="text/event-stream")


def sortByScore(object):
    return object["score"]


@app.route("/compare/<usernames_str>", methods=["GET"])
def compare(usernames_str: str):
    usernames = usernames_str.split(",")
    if len(usernames) > 10:
        return "Max 10 usernames", 400

    user_data = [get_user_info(username) for username in usernames]
    user_qual_scores = [get_user_quality(username) for username in usernames]
    user_exp_scores = [get_user_exerience(username, ai_prompt=False) for username in usernames]
    user_pop_scores = [get_user_popularity(username, ai_prompt=False) for username in usernames]
    
    
    # print(user_data, user_qual_scores, user_exp_scores, user_pop_scores)
    tot_user_scores = []
    # print(usernames)
    for i in range(len(usernames)):
        # print(f"{i=}")
        # print(user_qual_scores[i])
        # print(user_exp_scores[i])
        # print(user_pop_scores[i])
        tot_user_scores.append(round((user_qual_scores[i]["score"] + user_exp_scores[i]["score"] + user_pop_scores[i]["score"]) / 3))
        # print(user_scores[i])

    responseInfo = [
        {"user_data": user_data[i], "score": tot_user_scores[i]}
        for i in range(len(user_data))
    ]

    responseInfo.sort(key=sortByScore, reverse=True)

    response = make_response(responseInfo)

    return response
