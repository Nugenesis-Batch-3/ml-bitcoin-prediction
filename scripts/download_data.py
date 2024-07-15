# python packages
import sys
import os
import time
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# third-party packages
import pymongo
from pymongo import MongoClient
import yfinance as yf
from pycoingecko import CoinGeckoAPI
import pandas as pd
from api.config.config import Config
import requests
import quandl

client = MongoClient(Config.MONGO_URI)
db = client["nugenesis-bitcoin"]


def store_data(collection, data):
    collection = db[collection]
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)


def fetch_yahoo_finance_data(ticker="BTC-USD"):
    try:
        data = yf.download(ticker, start=None, end=None)
        data.reset_index(inplace=True)
        data.dict = data.to_dict("records")
        store_data("yahoo-finance", data.dict)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Blockchain data: {e}")


def fetch_blockchain_data():
    metrics = {
        "transactions_per_second": "transactions-per-second",
        "hash_rate": "hash-rate",
        "difficulty": "difficulty",
        "addresses": "n-unique-addresses",
    }

    start_date = datetime(2014, 1, 1)
    end_date = datetime.now()
    current_date = start_date

    while current_date < end_date:
        next_date = current_date + timedelta(days=365)
        if next_date > end_date:
            next_date = end_date

        for metric, endpoint in metrics.items():
            url = f"https://api.blockchain.info/charts/{endpoint}?timespan={365 if next_date < end_date else (end_date - current_date).days}days&format=json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()["values"]
                data_df = pd.DataFrame(data)
                data_df["timestamp"] = pd.to_datetime(data_df["x"], unit="s")
                data_df.drop(columns=["x"], inplace=True)
                data_df.rename(columns={"y": metric}, inplace=True)
                data_dict = data_df.to_dict("records")
                store_data(f"blockchain_{metric}", data_dict)
                print(
                    f"Fetched and stored {metric} data from {current_date.date()} to {next_date.date()}."
                )
            else:
                print(
                    f"Failed to fetch {metric} data. Status code: {response.status_code}, Error: {response.text}"
                )

        current_date = next_date


fetch_blockchain_data()


def fetch_nasdaq_bitcoin_data():
    try:
        api_key = "29s6xcjr1SS52UobEv8b"
        dataset_code = "BCHARTS/BITSTAMPUSD"
        url = f"https://data.nasdaq.com/api/v3/datasets/{dataset_code}/data.json?api_key={api_key}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            columns = data["dataset_data"]["column_names"]
            records = data["dataset_data"]["data"]
            data_df = pd.DataFrame(records, columns=columns)
            data_df["Date"] = pd.to_datetime(data_df["Date"])
            data_dict = data_df.to_dict("records")
            store_data("nasdaq", data_dict)
            print("Data fetched successfully")
        else:
            print(
                f"Failed to fetch data. Status code: {response.status_code}, Error: {response.text}"
            )
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Blockchain data: {e}")
