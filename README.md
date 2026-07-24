# Basic Binance Futures Trading Bot

A simple command-line trading bot built in Python using the **Binance Futures API**. The bot allows users to place **Market**, **Limit**, and **Stop-Limit** orders on USDT-M Futures, validates trading symbols, retrieves order status, and logs all activities for debugging.

> **Note:** This project is intended for educational purposes and demonstrates Binance API integration. It does not implement any automated trading strategy or market analysis.

---

## Features

- Supports **BUY** and **SELL** orders
- Supports the following order types:
  - MARKET
  - LIMIT
  - STOP_LIMIT
- Validates trading symbols before placing orders
- Retrieves and displays order execution status
- Logs requests, responses, and errors to `trading_bot.log`
- Includes exception handling for invalid input and Binance API errors
- Interactive command-line interface

---

## Project Structure

```
trading-bot/
│── trading_bot.py
│── config.py
│── README.md
```

---

## Requirements

- Python 3.8 or later
- Binance API Key and Secret
- python-binance

Install the required package:

```bash
pip install python-binance
```

---

## Configuration

Create a file named `config.py` in the project directory.

```python
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
```

The application imports these credentials automatically.

```python
from config import API_KEY, API_SECRET
```

---

## Running the Application

Run the bot using:

```bash
python trading_bot.py
```

You will see:

```
Welcome to the Basic Trading Bot (Binance Futures Testnet)

Commands:
  - BUY/SELL SYMBOL MARKET QUANTITY
  - BUY/SELL SYMBOL LIMIT PRICE QUANTITY
  - BUY/SELL SYMBOL STOP_LIMIT STOP_PRICE QUANTITY LIMIT_PRICE

Type 'exit' to quit.
```

---

## Example Commands

### Market Order

```
BUY BTCUSDT MARKET 0.001
```

Places a market buy order for **0.001 BTC**.

---

### Limit Order

```
BUY BTCUSDT LIMIT 115000 0.001
```

Places a limit buy order at **115000 USDT**.

---

### Stop-Limit Order

```
SELL BTCUSDT STOP_LIMIT 114500 0.001 114400
```

Where:

- Stop Price = 114500
- Quantity = 0.001
- Limit Price = 114400

---

## Sample Output

```
Order Placed Successfully:

Order ID: 123456789
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.001
Status: FILLED
```

---

## Logging

All activities are recorded in:

```
trading_bot.log
```

The log contains:

- User commands
- Successful orders
- Order status
- API errors
- Unexpected exceptions

---

## Error Handling

The bot handles:

- Invalid trading symbols
- Incorrect command formats
- Invalid quantity or price values
- Binance API exceptions
- Unexpected runtime errors

Examples:

```
Invalid symbol: ABCXYZ
```

```
Quantity must be positive.
```

```
Binance API Error: <error message>
```

---

## Technologies Used

- Python
- Binance Futures API
- python-binance
- Logging Module

---

## Security

API credentials are stored separately in `config.py` and imported into the application.

A sample configuration file:

```python
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
```

For security reasons, **do not commit your actual API credentials** to version control. Replace them locally before running the application.

---

## Limitations

This project demonstrates API integration only.

It does **not** include:

- Trading strategies
- Technical indicators
- Automated trading logic
- Risk management
- Portfolio management
- Machine learning models

All orders are entered manually through the command-line interface.

---

## Disclaimer

This project was developed for educational purposes to demonstrate integration with the Binance Futures API. Cryptocurrency trading involves significant financial risk. The author is not responsible for any financial losses resulting from the use of this software.
