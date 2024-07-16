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


# fetch_blockchain_data()


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


def fetch_blockchair_data():
    url = "https://api.blockchair.com/bitcoin/blocks"
    params = {
        "limit": 500,
        "fields": "id,time,transaction_count,output_total,fee_total,block_size",
    }
    all_data = []

    # Fetch data in batches
    start_date = datetime(2014, 1, 1)  # Adjust start date as needed
    end_date = datetime.now()

    while start_date < end_date:
        params["offset"] = 0  # Reset offset for each batch
        params["since"] = int(start_date.timestamp())

        response = requests.get(url, params=params)
        data = response.json().get("data", [])

        if not data:
            break

        all_data.extend(data)
        params["offset"] += 500  # Increase offset for next batch

        print(f"Fetched {len(data)} blocks, total fetched: {len(all_data)}")

        # Increment start_date for next batch (e.g., fetch data monthly)
        start_date += timedelta(days=30)  # Adjust interval as needed

    # Process and store data
    processed_data = []
    for entry in all_data:
        try:
            timestamp = datetime.fromtimestamp(int(entry["time"]))
            entry["timestamp"] = timestamp
            del entry["time"]
            processed_data.append(entry)
        except ValueError:
            print(f"Skipping entry with invalid timestamp: {entry}")

    store_data("blockchair", processed_data)
    print(f"Stored {len(processed_data)} blocks into MongoDB")


def fetch_cryptocompare_data():
    url = "https://min-api.cryptocompare.com/data/blockchain/histo/day"
    params = {
        "fsym": "BTC",
        "limit": 2000,
        "api_key": "d718d3e12f1bb85c3bfb27a1dc5e8844cae07c6d470db8f43d6b31c64681f258",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["Data"]

        data_to_store = []

        for item in data["Data"]:
            timestamp = datetime.fromtimestamp(item["time"])
            item["time"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            data_to_store.append(item)

        # Store only the "Data" array itself
        store_data("cryptocompare_v2", data_to_store)

        print(f"Stored {len(data_to_store)} entries from 'Data' into MongoDB")

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


def fetch_yahoo_finance_intraday_data(ticker="BTC-USD", years=10, interval="1h"):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)

        # Initialize an empty DataFrame to hold the combined data
        combined_data = pd.DataFrame()

        # Fetch data in chunks of less than 730 days
        while start_date < end_date:
            chunk_end_date = min(start_date + timedelta(days=729), end_date)
            print(f"Fetching data from {start_date} to {chunk_end_date}")

            # Fetch the data for the current chunk
            data = yf.download(
                ticker, start=start_date, end=chunk_end_date, interval=interval
            )
            combined_data = pd.concat([combined_data, data])

            # Move the start date to the next chunk
            start_date = chunk_end_date

        combined_data.reset_index(inplace=True)

        # Convert to dictionary
        data_dict = combined_data.to_dict("records")
        store_data("yahoo-finance-intraday", data_dict)
        print("Intraday data fetched successfully")

    except Exception as e:
        print(f"Error fetching Bitcoin data from Yahoo Finance: {e}")
