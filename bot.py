import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from flask import Flask
from threading import Thread
import os

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ENV VARIABLES
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask Web Server (Render Web Service)
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot Running Successfully!"

def run_web():
    web.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

# Pyrogram Bot
app = Client(
    "batch_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(_, message):

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🩺 NEET Batch 1", callback_data="batch1")],
        [InlineKeyboardButton("🩺 NEET Batch 2", callback_data="batch2")]
    ])

    await message.reply_text(
        "📚 Select Your Batch 👇",
        reply_markup=buttons
    )

@app.on_callback_query()
async def callbacks(_, query):

    if query.data == "batch1":
        await query.message.edit_text(
            "🩺 NEET Batch 1\n\n"
            "💰 Price: ₹200 (100⭐)\n\n"
            "Payment karne ke baad\n"
            "@Jatxchatbot par message karo.\n\n"
            "Admin payment verify karke access dega."
        )

    elif query.data == "batch2":
        await query.message.edit_text(
            "🩺 NEET Batch 2\n\n"
            "💰 Price: ₹200 (100⭐)\n\n"
            "Payment karne ke baad\n"
            "@Jatxchatbot par message karo.\n\n"
            "Admin payment verify karke access dega."
        )

if __name__ == "__main__":
    Thread(target=run_web).start()
    print("Bot Started...")
    app.run()