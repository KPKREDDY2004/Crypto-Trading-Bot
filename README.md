# Crypto-Trading-Bot

The Crypto Trading Bot in Python project, 

INTERN.PY, is a simplified trading bot designed to interact with the Binance Futures Testnet. The bot is built to handle two types of orders: 

market and limit. It uses environment variables, stored in a file named 

bot.env, to securely load API keys.

The project has the following key components:


Logging: It is configured to log all important events, including bot initialization, order parameters, and API responses, to both the console and a file named trading_bot.log. This is crucial for monitoring the bot's activities and troubleshooting issues.

BasicBot Class: This class is the core of the application. It initializes a connection to the Binance Testnet using provided API keys and the testnet=True flag. It also explicitly sets the API URL for the futures testnet to https://testnet.binancefuture.com/fapi. The class includes a helper method, _create_order, that handles placing orders and provides robust error handling for common issues like BinanceAPIException and BinanceRequestException.

Order Placement Methods: The BasicBot class contains two public methods: place_market_order and place_limit_order.


place_market_order: This method places a market order, which is executed immediately at the current market price.


place_limit_order: This method places a limit order, which is set to execute at a specific price or better. It uses a 

timeInForce of 'GTC' (Good 'Til Canceled), meaning the order remains active until it's filled or manually canceled.


Command-Line Interface (CLI): The script uses the argparse library to create a command-line interface, allowing users to specify the order type (market or limit), trading symbol (e.g., 'BTCUSDT'), side (BUY or SELL), and quantity directly when running the script. For limit orders, a price can also be specified.

The project is a practical example of building a foundational trading bot, demonstrating secure credential handling, API interaction, and robust error management.

Commands to Run the Project
Before running the script, ensure you have the required environment variables (

BINANCE_API_KEY and BINANCE_API_SECRET) configured in a file named bot.env in the same directory as the script.

To place a market order, use the following command structure. This example places a market buy order for 0.001 BTCUSDT:
python INTERN.PY market BTCUSDT BUY 0.001

To place a limit order, use the following command structure. This example places a limit sell order for 0.001 BTCUSDT at a price of 30,000:
python INTERN.PY limit BTCUSDT SELL 0.001 30000



