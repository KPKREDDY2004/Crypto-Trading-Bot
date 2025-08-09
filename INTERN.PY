import os
import logging
import argparse
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

# Load variables from your custom-named .env file
load_dotenv(dotenv_path='bot.env') # <-- THE ONLY CHANGE NEEDED

# --- 1. Logging Configuration --- 
# Sets up a logger to save all important events to a file named 'trading_bot.log'.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trading_bot.log"),
        logging.StreamHandler() # Also print logs to the console
    ]
)

# --- 2. The Main Bot Class --- [cite: 14]
class BasicBot:
    """
    A simplified trading bot to interact with Binance Futures Testnet.
    Fulfills the core requirements of the application task.
    """
    def __init__(self, api_key, api_secret):
        """
        Initializes the bot and connects to the Binance client.
        Args:
            api_key (str): Your Binance Testnet API key.
            api_secret (str): Your Binance Testnet API secret.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        
        # Initialize the client using testnet=True [cite: 15, 16]
        # The base URL for testnet is handled by the library when testnet=True.
        self.client = Client(self.api_key, self.api_secret, testnet=True)
        # Explicitly set the futures testnet URL for clarity [cite: 8]
        self.client.API_URL = 'https://testnet.binancefuture.com/fapi'
        
        logging.info("Bot initialized and connected to Binance Futures Testnet.")

    def _create_order(self, **kwargs):
        """A helper method to place an order and handle responses."""
        try:
            logging.info(f"Placing order with parameters: {kwargs}") # [cite: 11]
            order = self.client.futures_create_order(**kwargs)
            logging.info("Successfully placed order.")
            # Print and log the full order details and execution status [cite: 24]
            print("\n--- ✅ Order Success ---")
            print(f"  Symbol: {order.get('symbol')}")
            print(f"  OrderID: {order.get('orderId')}")
            print(f"  Side: {order.get('side')}")
            print(f"  Type: {order.get('type')}")
            print(f"  Quantity: {order.get('origQty')}")
            print(f"  Price: {order.get('price')}")
            print(f"  Status: {order.get('status')}")
            print("-----------------------\n")
            logging.info(f"API Response: {order}") # [cite: 11]
            return order
        except BinanceAPIException as e:
            # Handle specific API errors from Binance [cite: 25]
            logging.error(f"Binance API Error: {e.status_code} - {e.message}")
            logging.error(f"Failed to place order with parameters: {kwargs}") # [cite: 11]
            print(f"\n--- ❌ Order Failed: Binance API Error ---")
            print(f"  Status Code: {e.status_code}")
            print(f"  Message: {e.message}")
            print("-------------------------------------------\n")
        except BinanceRequestException as e:
            # Handle request errors (e.g., network issues) [cite: 25]
            logging.error(f"Binance Request Error: {e}")
            print(f"\n--- ❌ Order Failed: Request Error ---")
            print(f"  Message: {e}")
            print("---------------------------------------\n")
        except Exception as e:
            # Handle other potential errors
            logging.error(f"An unexpected error occurred: {e}")
            print(f"\n--- ❌ Order Failed: An unexpected error occurred ---")
            print(f"  Message: {e}")
            print("------------------------------------------------------\n")
        return None

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """
        Places a market order.
        Args:
            symbol (str): The trading pair (e.g., 'BTCUSDT').
            side (str): 'BUY' or 'SELL'. [cite: 21]
            quantity (float): The amount to trade.
        """
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'type': 'MARKET',
            'quantity': quantity
        }
        return self._create_order(**params)

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """
        Places a limit order.
        Args:
            symbol (str): The trading pair (e.g., 'BTCUSDT').
            side (str): 'BUY' or 'SELL'. [cite: 21]
            quantity (float): The amount to trade.
            price (float): The price at which to set the limit order.
        """
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'type': 'LIMIT',
            'quantity': quantity,
            'price': price,
            'timeInForce': 'GTC'  # Good 'Til Canceled
        }
        return self._create_order(**params)

# --- 3. Command-Line Interface (CLI) --- [cite: 23]
def main():
    """
    Parses command-line arguments to interact with the bot.
    """
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="A simplified Binance Futures trading bot.")
    subparsers = parser.add_subparsers(dest='order_type', help='The type of order to place', required=True)

    # --- Market Order Parser --- 
    parser_market = subparsers.add_parser('market', help='Place a market order')
    parser_market.add_argument('symbol', type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser_market.add_argument('side', type=str.upper, choices=['BUY', 'SELL'], help="Order side: BUY or SELL")
    parser_market.add_argument('quantity', type=float, help="Quantity to trade")

    # --- Limit Order Parser --- 
    parser_limit = subparsers.add_parser('limit', help='Place a limit order')
    parser_limit.add_argument('symbol', type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser_limit.add_argument('side', type=str.upper, choices=['BUY', 'SELL'], help="Order side: BUY or SELL")
    parser_limit.add_argument('quantity', type=float, help="Quantity to trade")
    parser_limit.add_argument('price', type=float, help="Price for the limit order")
    
    args = parser.parse_args()

    # --- Initialize and run the bot ---
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        logging.error("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        return

    bot = BasicBot(api_key=api_key, api_secret=api_secret)

    # --- Validate user input and execute the corresponding function --- [cite: 23]
    if args.order_type == 'market':
        bot.place_market_order(symbol=args.symbol, side=args.side, quantity=args.quantity)
    elif args.order_type == 'limit':
        bot.place_limit_order(symbol=args.symbol, side=args.side, quantity=args.quantity, price=args.price)

# --- 4. Script Execution ---
if __name__ == '__main__':
    main()