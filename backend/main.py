import os

from src.app import app
# Note: this file is only used for local development and not used when deploying through Cloud Run
#       The entrypoint for Cloud Run is tucon_backend/__init__.py
# app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))