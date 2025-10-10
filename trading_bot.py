import logging  # For saving logs to a file
from binance import Client  # The Binance tool
from binance.enums import *  # Extra Binance stuff
from binance.exceptions import BinanceAPIException  # For catching errors

# Set up logging (saves everything to trading_bot.log)
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        logging.info("Initialized Binance client in testnet mode")
    def validate_symbol(self, symbol):
        """Check if symbol is valid."""
        try:
            info = self.client.futures_exchange_info()
            symbols = [s['symbol'] for s in info['symbols']]
            if symbol.upper() in symbols:
                return True
            else:
                logging.error(f"Invalid symbol: {symbol}")
                return False
        except Exception as e:
            logging.error(f"Error validating symbol {symbol}: {str(e)}")
            return False
    def place_market_order(self, symbol, side, quantity):
        """Place a market order."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logging.info(f"Market order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"API error placing market order: {e.message}")
            raise
        except Exception as e:
            logging.error(f"Error placing market order: {str(e)}")
            raise
    def place_limit_order(self, symbol, side, quantity, price):
        """Place a limit order."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,  # Good Till Cancel
                quantity=quantity,
                price=price
            )
            logging.info(f"Limit order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"API error placing limit order: {e.message}")
            raise
        except Exception as e:
            logging.error(f"Error placing limit order: {str(e)}")
            raise
    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """Place a stop-limit order (bonus feature)."""
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_STOP,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=limit_price,  # Limit price
                stopPrice=stop_price  # Stop price
            )
            logging.info(f"Stop-Limit order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"API error placing stop-limit order: {e.message}")
            raise
        except Exception as e:
            logging.error(f"Error placing stop-limit order: {str(e)}")
            raise
    def get_order_status(self, symbol, order_id):
        """Get the status of an order."""
        try:
            status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            return status
        except Exception as e:
            logging.error(f"Error getting order status: {str(e)}")
            return None
    def run(self):
        """Command-line interface to accept and process orders."""
        print("Welcome to the Basic Trading Bot (Binance Futures Testnet)")
        print("Commands:")
        print("  - BUY/SELL SYMBOL MARKET QUANTITY")
        print("  - BUY/SELL SYMBOL LIMIT PRICE QUANTITY")
        print("  - BUY/SELL SYMBOL STOP_LIMIT STOP_PRICE QUANTITY LIMIT_PRICE (bonus)")
        print("Example: BUY BTCUSDT MARKET 0.001")
        print("Type 'exit' to quit.\n")

        while True:
            command = input("Enter command: ").strip()
            if command.lower() == 'exit':
                print("Exiting bot.")
                break
            parts = command.split()
            if len(parts) < 4:
                print("Invalid command. See examples above.")
                continue
            try:
                side_str = parts[0].upper()
                symbol = parts[1].upper()
                order_type = parts[2].upper()

                if side_str not in ['BUY', 'SELL']:
                    print("Side must be BUY or SELL.")
                    continue

                side = SIDE_BUY if side_str == 'BUY' else SIDE_SELL

                if not self.validate_symbol(symbol):
                    print(f"Invalid symbol: {symbol} (try BTCUSDT or ETHUSDT)")
                    continue
                if order_type == 'MARKET':
                    quantity = float(parts[3])
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue
                    logging.info(f"Request: {command}")
                    order = self.place_market_order(symbol, side, quantity)
                elif order_type == 'LIMIT':
                    if len(parts) != 5:
                        print("Limit order format: BUY/SELL SYMBOL LIMIT PRICE QUANTITY")
                        continue
                    price = float(parts[3])
                    quantity = float(parts[4])
                    if quantity <= 0 or price <= 0:
                        print("Quantity and price must be positive.")
                        continue
                    logging.info(f"Request: {command}")
                    order = self.place_limit_order(symbol, side, quantity, price)
                elif order_type == 'STOP_LIMIT':
                    if len(parts) != 6:
                        print("Stop-Limit format: BUY/SELL SYMBOL STOP_LIMIT STOP_PRICE QUANTITY LIMIT_PRICE")
                        continue
                    stop_price = float(parts[3])
                    quantity = float(parts[4])
                    limit_price = float(parts[5])
                    if quantity <= 0 or stop_price <= 0 or limit_price <= 0:
                        print("Quantity, stop price, and limit price must be positive.")
                        continue
                    logging.info(f"Request: {command}")
                    order = self.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                else:
                    print("Supported types: MARKET, LIMIT, STOP_LIMIT")
                    continue
                # Output order details
                print("\nOrder Placed Successfully:")
                print(f"  - Order ID: {order['orderId']}")
                print(f"  - Symbol: {order['symbol']}")
                print(f"  - Side: {order['side']}")
                print(f"  - Type: {order['type']}")
                print(f"  - Quantity: {order['origQty']}")
                if 'price' in order and order['price'] != '0.0':
                    print(f"  - Price: {order['price']}")
                if 'stopPrice' in order and order['stopPrice'] != '0.0':
                    print(f"  - Stop Price: {order['stopPrice']}")

                # Fetch and display execution status
                status = self.get_order_status(symbol, order['orderId'])
                if status:
                    print(f"  - Status: {status['status']}")
                    logging.info(f"Order status: {status['status']}")
                else:
                    print("  - Status: Unable to fetch (check logs).")

                print("\n")
            except ValueError:
                print("Invalid number in command (e.g., quantity or price must be floats).")
            except BinanceAPIException as e:
                print(f"Binance API Error: {e.message}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                logging.error(f"Unexpected error processing command: {str(e)}")


api_key = "zAgHhgJ5ZE9bs8BQ53Mf52locyBTTxmofF522jBigh468S6e58v0Yr661A2F0ojz"
api_secret = "b6DwsA4dC7XUDwzlhLttSocjcRczr5oIlXWWjazG1Wj3b8b7jGSVt3Ij9O6faWOC"

# Create the bot instance
bot = BasicBot(api_key, api_secret, testnet=True)

print("Bot initialized! No errors so far.")
bot.run()