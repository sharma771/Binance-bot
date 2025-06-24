import logging
from binance.client import Client
from binance.enums import *

# ✅ Set up logging
logging.basicConfig(filename='bot_log.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        try:
            self.client.ping()
            logging.info("✅ Connected to Binance Testnet")
        except Exception as e:
            logging.error(f"❌ Connection Error: {e}")
            print(f"❌ Could not connect to Binance Testnet: {e}")
            exit()

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == ORDER_TYPE_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_LIMIT:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                raise ValueError("❌ Unsupported order type")
            logging.info(f"✅ Order Placed: {order}")
            return order
        except Exception as e:
            logging.error(f"❌ Order Error: {e}")
            print(f"❌ Order Failed: {e}")
            return None

# ✅ CLI Execution
if __name__ == "__main__":
    print("🔐 Binance Testnet Trading Bot")

    api_key = input("Enter your Binance API Key: ")
    api_secret = input("Enter your Binance Secret Key (visible): ")

    bot = BasicBot(api_key, api_secret)

    symbol = input("Enter Trading Pair (e.g., BTCUSDT): ").upper()
    side = input("Order Side (BUY or SELL): ").upper()
    order_type = input("Order Type (MARKET or LIMIT): ").upper()
    quantity = float(input("Order Quantity: "))

    price = None
    if order_type == "LIMIT":
        price = input("Enter Limit Price: ")

    # Convert to Binance constants
    side_enum = SIDE_BUY if side == "BUY" else SIDE_SELL
    order_type_enum = ORDER_TYPE_MARKET if order_type == "MARKET" else ORDER_TYPE_LIMIT

    result = bot.place_order(symbol, side_enum, order_type_enum, quantity, price)

    if result:
        print("✅ Order Placed Successfully!")
        print(result)
    else:
        print("❌ Order was not placed. Check logs for more details.")
