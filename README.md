# Trading Bot Assignment

This repository contains a simplified trading bot. The bot interacts with the Binance API (via Demo Trading due to Testnet issues) to place market, limit, and stop-limit orders on USDT-M futures.

# Features
- Supports BUY and SELL orders.
- Handles MARKET, LIMIT, and STOP_LIMIT order types.
- Accepts commands via a command-line interface.
- Logs API requests, responses, and errors to `trading_bot.log`.
- Includes basic error handling.

# How to Run
1. Clone the repository: `git clone https://github.com/yourusername/trading-bot-assignment.git`
2. Create a `config.py` file with your API credentials:
   ```python
   api_key = "your_demo_trading_api_key"
   api_secret = "your_demo_trading_api_secret"
3. Install dependencies: pip install python-binance
4. Run the bot: python trading_bot.py
5. Enter commands (e.g., BUY BTCUSDT MARKET 0.01) or use the menu.

# Notes
Due to a 'server busy' issue on Binance Futures Testnet on Oct 10, 2025, I used Demo Trading (demo.binance.com) as a fallback. The bot was tested successfully with sample trades.
API keys are stored in config.py (not included for security).
