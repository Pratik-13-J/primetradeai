# app.py

import streamlit as st
from bot.orders import OrderManager

manager = OrderManager()

st.title("🚀 PrimeTradeAI Trading Dashboard")

menu = st.sidebar.selectbox(
    "Select Action",
    ["Trade", "Balance", "Positions", "History"]
)

if menu == "Balance":
    data = manager.get_account_balance()
    st.write("### Futures Balance")
    st.write(data)

elif menu == "Positions":
    positions = manager.get_open_positions()
    st.write("### Open Positions")
    st.write(positions)

elif menu == "History":
    trades = manager.get_trade_history()
    st.write("### Trade History")
    st.write(trades)

elif menu == "Trade":
    st.write("### Place Trade")

    symbol = st.text_input("Symbol", "BTCUSDT")
    side = st.selectbox("Side", ["BUY", "SELL"])
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
    quantity = st.number_input("Quantity", min_value=0.0)

    price = None
    if order_type == "LIMIT":
        price = st.number_input("Price", min_value=0.0)

    if st.button("Place Order"):
        result = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            wait_for_fill=True
        )
        st.success("Order Result")
        st.write(result)