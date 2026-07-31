import os
import requests
from dotenv import load_dotenv

load_dotenv()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Welcome to Heng Store\n\n"
        "Commands:\n"
        "/balance - Check balance\n"
        "/games - View games"
    )
    await update.message.reply_text(text)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(
            f"{BASE_URL}/balance",
            headers=HEADERS,
            timeout=10
        )

        data = r.json()

        if data.get("ok"):
            await update.message.reply_text(
                f"💰 Balance: {data['balance']} {data['currency']}"
            )
        else:
            await update.message.reply_text(
                "❌ Failed to get balance."
            )

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(
            f"{BASE_URL}/catalogue",
            headers=HEADERS,
            timeout=10
        )

        data = r.json()

        if not data.get("ok"):
            await update.message.reply_text("❌ Unable to load games.")
            return

        text = "🎮 Available Games\n\n"

        for game in data["games"]:
            text += f"• {game['name']} ({game['code']})\n"

        await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("games", games))

import asyncio

# ... your other bot setup code ...

if __name__ == '__main__':
    # Add these two lines to explicitly set the loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Now run the bot
    app.run_polling()



