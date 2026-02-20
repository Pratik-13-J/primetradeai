# interactive.py

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)

console = Console()
manager = OrderManager()


def show_balance():
    data = manager.get_account_balance()

    table = Table(title="Futures Balance")
    table.add_column("Asset")
    table.add_column("Wallet Balance")
    table.add_column("Available Balance")

    table.add_row(
        data["asset"],
        str(data["walletBalance"]),
        str(data["availableBalance"]),
    )

    console.print(table)


def show_positions():
    positions = manager.get_open_positions()

    if not positions:
        console.print("[yellow]No open positions.[/yellow]")
        return

    table = Table(title="Open Positions")
    table.add_column("Symbol")
    table.add_column("Position Amt")
    table.add_column("Entry Price")
    table.add_column("Unrealized PnL")

    for pos in positions:
        table.add_row(
            pos["symbol"],
            str(pos["positionAmt"]),
            str(pos["entryPrice"]),
            str(pos["unrealizedProfit"]),
        )

    console.print(table)


def place_trade():
    symbol = Prompt.ask("Enter Symbol (e.g. BTCUSDT)")
    side = Prompt.ask("Enter Side (BUY/SELL)")
    order_type = Prompt.ask("Order Type (MARKET/LIMIT)")
    quantity = FloatPrompt.ask("Quantity")

    price = None
    if order_type.upper() == "LIMIT":
        price = FloatPrompt.ask("Limit Price")

    # Validation
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)

    console.print("[blue]Placing Order...[/blue]")

    result = manager.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        wait_for_fill=True
    )

    console.print(result)


def show_history():
    trades = manager.get_trade_history()

    if not trades:
        console.print("[yellow]No trades found.[/yellow]")
        return

    table = Table(title="Trade History")
    table.add_column("Time")
    table.add_column("Symbol")
    table.add_column("Side")
    table.add_column("Qty")
    table.add_column("Price")

    for trade in trades:
        table.add_row(
            str(trade["time"]),
            trade["symbol"],
            trade["side"],
            str(trade["quantity"]),
            str(trade["price"]),
        )

    console.print(table)


def main_menu():
    while True:
        console.print("\n[bold cyan]🚀 PrimeTradeAI Trading Terminal[/bold cyan]")
        console.print("1) Place Trade")
        console.print("2) Check Balance")
        console.print("3) View Positions")
        console.print("4) Trade History")
        console.print("5) Exit")

        choice = Prompt.ask("Select option")

        if choice == "1":
            place_trade()
        elif choice == "2":
            show_balance()
        elif choice == "3":
            show_positions()
        elif choice == "4":
            show_history()
        elif choice == "5":
            console.print("[green]Exit![/green]")
            break
        else:
            console.print("[red]Invalid choice[/red]")


if __name__ == "__main__":
    main_menu()