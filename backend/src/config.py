import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GITHUB_TOKEN:
    raise ValueError("No GITHUB_TOKEN set for Flask application")
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY set for Flask application")
