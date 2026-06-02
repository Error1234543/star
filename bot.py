from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 12345
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

app = Client(
    "batch_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(_, message):

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🩺 NEET Batch 1",
                callback_data="batch1"
            )
        ],
        [
            InlineKeyboardButton(
                "🩺 NEET Batch 2",
                callback_data="batch2"
            )
        ]
    ])

    await message.reply_text(
        "Select Your Batch 👇",
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

app.run()
