from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env")


class Config:
    FLASK_APP = os.getenv("FLASK_APP")
    FLASK_ENV = os.getenv("FLASK_ENV")
    MONGO_URI = os.getenv("MONGO_URI")
