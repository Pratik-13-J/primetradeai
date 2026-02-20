# 🚀 Binance Futures Testnet Trading Bot

A modular and professional Python trading bot built for **Binance USDT-M Futures Testnet**.

This project demonstrates clean architecture, structured logging, proper error handling, and a professional command-line interface using Typer.

---

### 🎯 Project Objective

Build a structured and reusable Python trading application that:

Places orders on Binance Futures Testnet

Handles API errors and network failures

Logs requests and responses

Provides a professional CLI interface

Follows clean code architecture principles

### 🏗 Architecture Overview

The project follows a layered design pattern:

CLI Layer (main.py)
↓
Order Manager (orders.py)
↓
API Client Wrapper (client.py)
↓
Binance Futures Testnet

### 📂 Project Structure

primetradeai/
│
├── bot/
│ ├── client.py # Binance API abstraction layer
│ ├── orders.py # Order placement & execution polling
│ ├── validators.py # CLI input validation
│ ├── logging_config.py # Structured logging setup
│
├── logs/ # Runtime log files
├── main.py # Professional Typer CLI entry point
├── interactive.py # Interactive trading terminal
├── app.py # Streamlit web dashboard
├── requirements.txt
├── README.md
└── .gitignore

## 📌 Features

### ✅ Core Trading Features

- Place **MARKET** and **LIMIT** orders
- Support for both **BUY** and **SELL**
- Automatic order status polling (waits for fill)
- Structured logging of API requests and responses
- Robust exception handling
- Input validation

### ✅ Account Utilities

- Check Futures **USDT balance**
- View **open positions**
- View **trade history**

### ✅ Structured Logging

Logs stored in: logs/trading_bot.log
Logs include:
API request parameters
Binance API responses
Order status updates
Execution confirmation
Error logs (API & network)

### ✅ Error Handling

The bot handles:
Invalid user inputs
Binance API exceptions
Network failures
Empty API responses
Order timeout conditions
Missing required parameters

## How to Run & Visualize

### ✅ Professional CLI (Typer-based)

Structured command system similar to production tools:

```bash
python main.py --help # show help
python main.py balance # Check Balance
python main.py positions # View Positions
python main.py history # View Trade History
python main.py trade --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 # Place Market Order
python main.py trade --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000 # Place Limit Order
```

### Interactive Trading Terminal (interactive.py)

Provides a menu-driven trading experience:

1. Place Trade
2. Check Balance
3. View Positions
4. Trade History
5. Exit

Run: python interactive.py

### Streamlit Web Dashboard (app.py)

Lightweight browser-based trading interface.

Run: streamlit run app.py

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

git clone <repository-link>
cd primetradeai

### 2️⃣ Create Virtual Environment

Windows:
python -m venv venv
venv\Scripts\activate

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Configure API Keys

Create a .env file in the project root:
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret_key
This project is configured for: https://testnet.binancefuture.com

### 📦 Dependencies

Python 3.9+
python-binance
typer
rich
python-dotenv
streamlit (optional)
python-dotenv

## 👨‍💻 Author

Developed as part of a Python Developer internship technical assessment to demonstrate:
Backend system design
API integration
CLI application architecture
Logging & observability
Trading workflow automation
