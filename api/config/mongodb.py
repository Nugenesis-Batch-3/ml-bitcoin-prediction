from pymongo import MongoClient
from api.config.config import Config


def get_database():
    connection_string = Config.MONGO_URI
    client = MongoClient(connection_string)
    return client.get_database(name="nugenesis-bitcoin")
