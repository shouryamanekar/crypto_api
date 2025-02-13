import os
import requests
import time
import threading
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger
from flask_pymongo import PyMongo

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
db = mongo.db

# Initialize Swagger UI
app.config["SWAGGER"] = {"title": "Crypto API", "uiversion": 3}
swagger = Swagger(app)

# CoinMarketCap API Configuration
API_KEY = os.getenv("CMC_API_KEY")
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}

# Fetch and Store Data in MongoDB
@app.route("/api/fetch", methods=["GET"])
def fetch_crypto_data():
    """
    Fetches cryptocurrency data and stores it in MongoDB.
    ---
    responses:
      200:
        description: Successfully fetched and stored crypto data.
      500:
        description: Failed to fetch data.
    """
    params = {"start": "1", "limit": "50", "convert": "USD"}
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()["data"]

    # Clear existing data
    db.cryptos.delete_many({})

    # Insert new data
    crypto_list = []
    for coin in data:
        crypto_list.append({
            "name": coin["name"],
            "symbol": coin["symbol"],
            "price": coin["quote"]["USD"]["price"],
            "market_cap": coin["quote"]["USD"]["market_cap"],
            "volume_24h": coin["quote"]["USD"]["volume_24h"],
            "percent_change_24h": coin["quote"]["USD"]["percent_change_24h"],
        })

    db.cryptos.insert_many(crypto_list)

    return jsonify({"message": "Data Fetched and Stored!"})

# Create an API route to show full market data in JSON format
@app.route("/api/market_data", methods=["GET"])
def get_market_data():
    """
    Returns full cryptocurrency market data in JSON format.
    ---
    responses:
      200:
        description: A JSON list of cryptocurrency data.
    """
    cryptos = list(db.cryptos.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return jsonify(cryptos)

# Background Thread to Run Fetch Every 5 Minutes
def run_fetch_periodically():
    while True:
        print("Auto Fetch: Fetching new crypto data...")
        try:
            response = requests.get("http://127.0.0.1:5000/api/fetch")
            if response.status_code == 200:
                print("Successfully fetched and stored crypto data.")
            else:
                print("Fetch request failed:", response.text)
        except Exception as e:
            print("Error fetching data:", e)
        
        time.sleep(300)  # Wait 5 minutes before running again

# Start the background fetch thread
fetch_thread = threading.Thread(target=run_fetch_periodically, daemon=True)
fetch_thread.start()

if __name__ == "__main__":
    # Start Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
