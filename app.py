from flask import Flask
from api.config.mongodb import get_database
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

app = Flask(__name__)
FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")


@app.route("/")
def home():
    return "Welcome to the Bitcoin Prediction API!"


@app.before_request
def initialize_database():
    print("Initializing database...")
    db = get_database()
    print("Database initialized.")
    collections = db.list_collection_names()
    print("Collections in the database:", collections)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, load_dotenv=True)


print("App started.")
print("FLASK_APP:", FLASK_APP)
print("FLASK_ENV:", FLASK_ENV)
