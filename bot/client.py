# bot/client.py

import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

load_dotenv()


class BinanceFuturesClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        api_key = os.getenv("BINANCE_API_KEY")
        secret_key = os.getenv("BINANCE_SECRET_KEY")

        if not api_key or not secret_key:
            raise ValueError("API keys not found in .env file")

        self.client = Client(api_key, secret_key, testnet=True)
        self.logger.info("Binance Futures Testnet client initialized")

    def get_balance(self) -> list:
        try:
            self.logger.info("Fetching Futures account balance")
            response = self.client.futures_account_balance()
            return response

        except Exception:
            self.logger.exception("Error fetching account balance")
            raise

    def get_positions(self) -> list:
        try:
            self.logger.info("Fetching Futures positions")
            response = self.client.futures_position_information()
            return response

        except Exception:
            self.logger.exception("Error fetching positions")
            raise

    def create_order(self, params: dict) -> dict:
        try:
            self.logger.info(f"Sending order request: {params}")
            response = self.client.futures_create_order(**params)
            self.logger.info(f"Order response: {response}")
            return response

        except BinanceAPIException as e:
            self.logger.error(f"Binance API Error: {e.message}")
            raise

        except BinanceRequestException as e:
            self.logger.error(f"Network Error: {str(e)}")
            raise

        except Exception:
            self.logger.exception("Unexpected error during order placement")
            raise

    def get_order(self, symbol: str, order_id: int) -> dict:
        try:
            response = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            return response

        except Exception:
            self.logger.exception("Error fetching order status")
            raise
    
    def get_trade_history(self, symbol: str = None):
        try:
            self.logger.info("Fetching trade history")

            if symbol:
                response = self.client.futures_account_trades(symbol=symbol)
            else:
                response = self.client.futures_account_trades()

            return response

        except Exception:
            self.logger.exception("Error fetching trade history")
            raise