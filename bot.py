from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "BatchBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 NEET Batch 1", callback_data="batch1")],
        [InlineKeyboardButton("📚 NEET Batch 2", callback_data="batch2")],
    ])

    await message.reply_text(
        "🔥 Welcome!\n\nSelect Your Batch 👇",
        reply_markup=buttons
    )

@app.on_callback_query()
async def callback(client, query):

    if query.data == "batch1":

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Buy Now (100 Stars)", callback_data="buy1")],
            [InlineKeyboardButton("🔙 Back", callback_data="home")]
        ])

        await query.message.edit_text(
            "📚 NEET Batch 1\n\n"
            "✅ HD Lectures\n"
            "✅ Notes\n"
            "✅ Tests\n\n"
            "💰 Price: 100 ⭐",
            reply_markup=buttons
        )

    elif query.data == "batch2":

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Buy Now (100 Stars)", callback_data="buy2")],
            [InlineKeyboardButton("🔙 Back", callback_data="home")]
        ])

        await query.message.edit_text(
            "📚 NEET Batch 2\n\n"
            "✅ HD Lectures\n"
            "✅ Notes\n"
            "✅ Tests\n\n"
            "💰 Price: 100 ⭐",
            reply_markup=buttons
        )

    elif query.data.startswith("buy"):

        await query.message.edit_text(
            "⭐ Payment Instructions\n\n"
            "100 Stars payment complete karne ke baad\n\n"
            "📩 Screenshot bhejo:\n"
            "@Jatxchatbot\n\n"
            "Admin verification ke baad access diya jayega."
        )

    elif query.data == "home":

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 NEET Batch 1", callback_data="batch1")],
            [InlineKeyboardButton("📚 NEET Batch 2", callback_data="batch2")]
        ])

        await query.message.edit_text(
            "🔥 Welcome!\n\nSelect Your Batch 👇",
            reply_markup=buttons
        )

app.run()