from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

import os

TOKEN = os.environ['TOKEN']


def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT'
    res = requests.get(url)
    data = res.json()
    return f"{symbol.upper()}: ${data['price']}"

def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! نماد رمزارز مورد نظرتو با / بنویس، مثل /BTC')

def handle_symbol(update: Update, context: CallbackContext):
    symbol = update.message.text[1:].upper()
    try:
        price = get_price(symbol)
        update.message.reply_text(price)
    except:
        update.message.reply_text("نماد اشتباهه یا مشکلی در دریافت اطلاعات هست.")

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler(None, handle_symbol))

updater.start_polling()
updater.idle()
