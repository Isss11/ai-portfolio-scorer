from src.app import app

@app.route("/", methods=["GET"])
def index():
    return f"Welcome to PyroMetric backend!"

@app.route("/generalFeedback", methods=["POST"])
def generalFeedback():    
    return f"Placeholder to query the Gemini API"
