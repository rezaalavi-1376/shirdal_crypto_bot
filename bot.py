import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime, time

# ENV config
TOKEN = os.environ['TOKEN']

# Get CoinGecko coin ID from symbol
def get_coin_id(symbol):
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        coins = response.json()
        for coin in coins:
            if coin["symbol"].lower() == symbol.lower():
                return coin["id"]
    return None

# Get price from CoinGecko
def get_price(symbol):
    coin_id = get_coin_id(symbol)
    if coin_id:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get(coin_id, {}).get("usd", None)
    return None

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is running. Use /btc, /eth, or any other coin symbol to get price.")

# Handle all coin commands
def handle_command(update: Update, context: CallbackContext):
    symbol = update.message.text[1:].strip().upper()
    price = get_price(symbol)
    if price:
        update.message.reply_text(f"💰 {symbol.upper()} price: ${price}")
    else:
        update.message.reply_text("❌ Coin not found or unsupported.")

# Daily report of selected coins
def send_daily_prices(context: CallbackContext):
    important_coins = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP']
    message = f"📊 Daily Market Report - {datetime.utcnow().strftime('%Y-%m-%d')}\n\n"
    for symbol in important_coins:
        price = get_price(symbol)
        if price:
            message += f"{symbol}: ${price}\n"
        else:
            message += f"{symbol}: N/A\n"
    if CHAT_ID:
        context.bot.send_message(chat_id=CHAT_ID, text=message)

# Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands and messages
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.command, handle_command))

    # Daily job at 10:00 UTC
    job = updater.job_queue
    job.run_daily(send_daily_prices, time=time(10, 0))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
