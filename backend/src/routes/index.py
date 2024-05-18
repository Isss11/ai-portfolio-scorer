from flask import json, request
from src.app import app

@app.route("/", methods=["GET"])
def index():
    return f"Welcome to PyroMetric backend!"

@app.route("/generalFeedback", methods=["POST"])
def generalFeedback():    
    return f"Placeholder to query the Gemini API"

@app.route("/score-individual/", methods=["GET"])
def score_individual():
    def generate():
        yield json.dumps({"category": "metadata", "username": "user" })
        yield json.dumps({"score": 0})

    return app.response_class(generate(), mimetype="text/event-stream")

@app.route("/compareProfiles", methods=["POST"])
def compareProfiles():
    links = []
    
    try:
        linksString = request.json['profileLinks'].replace(" ", "")
        links = linksString.split("\n")
        
        # Deal with border case to remove all empty links
        emptyLinksRemoved = False
        
        while not emptyLinksRemoved:
            try:
                links.remove('')
            except:
                print("Removed all empty links, if they ever existed.")
                emptyLinksRemoved = True
                
    except:
        print("An error has occurrred")
        
    print(links)
    
    return f"Placeholder response to compare users."
