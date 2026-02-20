# bot/orders.py

import logging
import time
from bot.client import BinanceFuturesClient
from datetime import datetime

class OrderManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = BinanceFuturesClient()

    # -------------------------------
    # BALANCE
    # -------------------------------
    def get_account_balance(self):
        balances = self.client.get_balance()

        for asset in balances:
            if asset["asset"] == "USDT":
                return {
                    "asset": "USDT",
                    "walletBalance": float(asset["balance"]),
                    "availableBalance": float(asset["availableBalance"]),
                }

        return None

    # -------------------------------
    # POSITIONS
    # -------------------------------
    def get_open_positions(self):
        positions = self.client.get_positions()
        open_positions = []

        for pos in positions:
            if float(pos.get("positionAmt", 0)) != 0:
                open_positions.append({
                    "symbol": pos.get("symbol"),
                    "positionAmt": float(pos.get("positionAmt", 0)),
                    "entryPrice": float(pos.get("entryPrice", 0)),
                    "unrealizedProfit": float(pos.get("unRealizedProfit", 0)),
                    "leverage": pos.get("leverage", "N/A"),
                })

        return open_positions

    # -------------------------------
    # ORDER PLACEMENT
    # -------------------------------
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None,
        wait_for_fill: bool = True,
        timeout: int = 20
    ) -> dict:

        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        response = self.client.create_order(params)

        if not response:
            raise Exception("Empty response from Binance")

        order_id = response.get("orderId")

        if not order_id:
            raise Exception("Order ID missing in Binance response")

        status = response.get("status")
        self.logger.info(f"Order placed: {order_id}, status: {status}")

        # Poll for fill
        if wait_for_fill:
            start_time = time.time()

            while time.time() - start_time < timeout:
                order_status = self.client.get_order(symbol, order_id)
                current_status = order_status.get("status")

                if current_status == "FILLED":
                    return {
                        "orderId": order_id,
                        "status": current_status,
                        "executedQty": float(order_status.get("executedQty", 0)),
                        "avgPrice": float(order_status.get("avgPrice", 0)),
                    }

                elif current_status in ["CANCELED", "REJECTED", "EXPIRED"]:
                    return {
                        "orderId": order_id,
                        "status": current_status,
                        "executedQty": float(order_status.get("executedQty", 0)),
                        "avgPrice": float(order_status.get("avgPrice", 0)),
                    }

                time.sleep(2)

            return {
                "orderId": order_id,
                "status": "TIMEOUT",
                "executedQty": 0,
                "avgPrice": 0,
            }

        return {
            "orderId": order_id,
            "status": status,
            "executedQty": float(response.get("executedQty", 0)),
            "avgPrice": float(response.get("avgPrice", 0)),
        }

    def get_trade_history(self, symbol: str = None):
        trades = self.client.get_trade_history(symbol)

        formatted_trades = []

        for trade in trades:
            formatted_trades.append({
                "symbol": trade.get("symbol"),
                "side": trade.get("side"),
                "quantity": float(trade.get("qty", 0)),
                "price": float(trade.get("price", 0)),
                "realizedPnl": float(trade.get("realizedPnl", 0)),
                "time": datetime.fromtimestamp(trade.get("time") / 1000),
            })

        return formatted_trades