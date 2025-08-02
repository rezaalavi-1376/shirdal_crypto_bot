import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime

# دریافت توکن ربات از متغیر محیطی
TOKEN = os.environ['TOKEN']

# تبدیل symbol به id در CoinGecko (مثل BTC → bitcoin)
def get_coin_id(symbol):
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        coins = response.json()
        for coin in coins:
            if coin["symbol"].lower() == symbol.lower():
                return coin["id"]
    return None

# دریافت قیمت ارز
def get_price(symbol):
    coin_id = get_coin_id(symbol)
    if coin_id:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get(coin_id, {}).get("usd", None)
    return None

# شروع ربات
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ ربات فعال است.\nبرای دریافت قیمت بنویس: /btc یا /eth یا /هرارزی")

# پاسخ به هر پیام که با / شروع شود (مثلاً /btc)
def handle_command(update: Update, context: CallbackContext):
    symbol = update.message.text[1:].strip().upper()
    price = get_price(symbol)
    if price:
        update.message.reply_text(f"💰 قیمت {symbol.upper()} الان: ${price}")
    else:
        update.message.reply_text("❌ متأسفم! این ارز پیدا نشد یا توسط CoinGecko پشتیبانی نمی‌شود.")

# اجرای ربات
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.command, handle_command))  # همه دستورات مثل /btc /sol و...

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

