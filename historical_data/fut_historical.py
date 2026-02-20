# get_futures_historical.py

import logging
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv

load_dotenv()

# Directory for storing historical data
# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to historical_data folder
HISTORICAL_DATA_DIR = os.path.join(BASE_DIR, "historical_data")

# Create folder if it doesn't exist
os.makedirs(HISTORICAL_DATA_DIR, exist_ok=True)

# Fetching process logging info
log_file_path = os.path.join(HISTORICAL_DATA_DIR, "futures_historical.log")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Now fetch keys
api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

if not api_key or not secret_key:
    raise ValueError("API keys not found. Check your .env file.")

client = Client(api_key, secret_key)


def get_futures_klines(symbol: str, interval: str, start_str: str):
    try:
        logging.info(f"Fetching FUTURES data: {symbol}, {interval}, {start_str}")

        klines = client.futures_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_str
        )

        if not klines:
            raise ValueError("No data returned from Binance.")

        ALL_COLUMNS = [
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume",
            "ignore"
        ]

        REQUIRED_COLUMNS = [
            "open_time","open","high","low","close","volume","close_time" 
        ]


        df = pd.DataFrame(klines, columns=ALL_COLUMNS)
        df = df[REQUIRED_COLUMNS]

        df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
        df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')

        numeric_cols = ["open", "high", "low", "close", "volume"]
        df[numeric_cols] = df[numeric_cols].astype(float)

        logging.info("Futures data fetched successfully")
        return df

    except BinanceAPIException as e:
        logging.error(f"Binance API Error: {e.message}")
        print("API Error:", e.message)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print("Error:", str(e))


if __name__ == "__main__":
    df = get_futures_klines(
        symbol="BTCUSDT",
        interval=Client.KLINE_INTERVAL_1DAY,
        start_str="1 Jan, 2025"
    )

    if df is not None:
        csv_path = os.path.join(HISTORICAL_DATA_DIR, "btc_futures_data.csv")
        df.to_csv(csv_path, index=False)
        print(df.head())