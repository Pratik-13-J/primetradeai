# main.py

import typer
import logging
from rich.console import Console
from rich.table import Table
from bot.logging_config import setup_logging
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    
    validate_quantity,
    validate_price,
)
from binance.exceptions import BinanceAPIException, BinanceRequestException

app = typer.Typer(help="🚀 Binance Futures Testnet Trading Bot")
console = Console()


# -------------------------------
# BALANCE COMMAND
# -------------------------------
@app.command()
def balance():
    """Show Futures USDT balance"""
    setup_logging()
    manager = OrderManager()

    try:
        data = manager.get_account_balance()

        table = Table(title="Futures Balance")
        table.add_column("Asset", style="cyan")
        table.add_column("Wallet Balance", style="green")
        table.add_column("Available Balance", style="yellow")

        table.add_row(
            data["asset"],
            str(data["walletBalance"]),
            str(data["availableBalance"]),
        )

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


# -------------------------------
# POSITIONS COMMAND
# -------------------------------
@app.command()
def positions():
    """Show open futures positions"""
    setup_logging()
    manager = OrderManager()

    try:
        positions = manager.get_open_positions()

        if not positions:
            console.print("[bold yellow]No open positions.[/bold yellow]")
            return

        table = Table(title="Open Positions")
        table.add_column("Symbol", style="cyan")
        table.add_column("Position Amt", style="green")
        table.add_column("Entry Price", style="yellow")
        table.add_column("Unrealized PnL", style="magenta")
        table.add_column("Leverage", style="red")

        for pos in positions:
            table.add_row(
                pos["symbol"],
                str(pos["positionAmt"]),
                str(pos["entryPrice"]),
                str(pos["unrealizedProfit"]),
                str(pos["leverage"]),
            )

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


# -------------------------------
# TRADE HISTORY COMMAND
# -------------------------------
@app.command()
def history(symbol: str = typer.Option(None, help="Filter by symbol")):
    """Show trade history"""
    setup_logging()
    manager = OrderManager()

    try:
        trades = manager.get_trade_history(symbol)

        if not trades:
            console.print("[bold yellow]No trades found.[/bold yellow]")
            return

        table = Table(title="Trade History")
        table.add_column("Time", style="cyan")
        table.add_column("Symbol", style="green")
        table.add_column("Side", style="yellow")
        table.add_column("Quantity", style="magenta")
        table.add_column("Price", style="white")

        for trade in trades:
            table.add_row(
                str(trade["time"]),
                trade["symbol"],
                trade["side"],
                str(trade["quantity"]),
                str(trade["price"]),
            )

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


# -------------------------------
# TRADE COMMAND
# -------------------------------
@app.command()
def trade(
    symbol: str = typer.Option(..., help="Trading symbol e.g. BTCUSDT"),
    side: str = typer.Option(..., help="BUY or SELL"),
    type: str = typer.Option(..., help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: float = typer.Option(None, help="Required for LIMIT orders"),
):
    """Place a trade order"""

    setup_logging()
    logger = logging.getLogger(__name__)
    manager = OrderManager()

    try:
        # Validation
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(type)
        quantity = validate_quantity(quantity)
        price = validate_price(price, order_type)

        console.print("\n[bold blue]Placing Order...[/bold blue]")

        result = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            wait_for_fill=True
        )

        table = Table(title="Order Result")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Order ID", str(result["orderId"]))
        table.add_row("Status", result["status"])
        table.add_row("Executed Qty", str(result["executedQty"]))
        table.add_row("Avg Price", str(result["avgPrice"]))

        console.print(table)

        if result["status"] == "FILLED":
            console.print("[bold green]✅ Order executed successfully![/bold green]")
        elif result["status"] == "TIMEOUT":
            console.print("[bold yellow]⏳ Order not filled within timeout.[/bold yellow]")
        else:
            console.print(f"[bold red]Final Status: {result['status']}[/bold red]")

    except ValueError as e:
        logger.error(f"Validation Error: {str(e)}")
        console.print(f"[bold red]Validation Error: {e}[/bold red]")

    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e.message}")
        console.print(f"[bold red]Binance API Error: {e.message}[/bold red]")

    except BinanceRequestException:
        console.print("[bold red]Network Error. Check connection.[/bold red]")

    except Exception:
        logger.exception("Unexpected error occurred")
        console.print("[bold red]Unexpected error occurred. Check logs.[/bold red]")


if __name__ == "__main__":
    app()