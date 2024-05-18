from flask import Flask, json
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Create the Flask app instance
app = Flask(__name__)

CORS(app, supports_credentials=True)

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'secret' 
jwt = JWTManager(app)

# Import routes after app creation to avoid circular imports
# ==== Routes ====
from src.routes import index

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()

    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
