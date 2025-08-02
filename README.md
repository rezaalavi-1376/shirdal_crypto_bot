# shirdal_crypto_bot
shirdalcrypto ربات تلگرام رمز ارز
# Shirdal Crypto Bot 🦎💰

A simple Telegram bot for real-time crypto prices using CoinGecko API. Deployed on [Render.com](https://render.com), kept alive with Flask.

## 🚀 Setup

1. Clone the repo:
https://github.com/rezaalavi-1376/shirdal_crypto_bot


2. Add your Telegram Bot Token:
Set `TOKEN` and optionally `CHAT_ID` as environment variables on Render.

3. Deploy to Render:
- Use **Python environment**
- Add `Procfile`, `runtime.txt`, and `requirements.txt`
- Point your uptime monitor (like UptimeRobot) to the root URL (`/`) to keep bot alive.

## 🔧 Features

- `/btc`, `/eth`, etc. for current prices
- Daily market report at 10:00 UTC
- Web server endpoint for uptime

---

Feel free to fork and customize!
