import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    PreCheckoutQueryHandler, CallbackQueryHandler, filters, ContextTypes
)
from flask import Flask, request

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN      = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
OWNER_ID       = int(os.environ.get("OWNER_ID", "8226637107"))
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "@Jatxchatbot")
WEBHOOK_URL    = os.environ.get("WEBHOOK_URL", "")  # Render URL, e.g. https://jatx-bot.onrender.com
STARS_AMOUNT   = 100

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

flask_app = Flask(__name__)

# ─── /start ───────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("⭐ Buy Material - 100 Stars (₹200)", callback_data="buy")]]
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        f"🎯 *Exclusive Study Material*\n\n"
        f"📦 Premium material milega ek baar payment ke baad.\n\n"
        f"💰 *Price:* 100 ⭐ Telegram Stars (≈ ₹200)\n\n"
        f"Niche button dabao aur payment karo! ✅",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─── BUTTON ───────────────────────────────────────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "buy":
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="📚 Premium Study Material",
            description="Payment ke baad exclusive material ka access milega.",
            payload="material_purchase",
            currency="XTR",
            prices=[LabeledPrice("Premium Material", STARS_AMOUNT)],
            provider_token=""
        )

# ─── PRE-CHECKOUT ─────────────────────────────────────────────────────────────
async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload == "material_purchase":
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Kuch galat ho gaya, dobara try karo.")

# ─── SUCCESSFUL PAYMENT ───────────────────────────────────────────────────────
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    payment = update.message.successful_payment
    stars_paid = payment.total_amount
    charge_id  = payment.telegram_payment_charge_id

    # User ko message
    await update.message.reply_text(
        f"✅ *Payment Successful!*\n\n"
        f"Aapne *{stars_paid} ⭐ Stars* pay kar diye!\n\n"
        f"🔓 Access ke liye is bot mein message karo:\n"
        f"👉 {OWNER_USERNAME}\n\n"
        f"_Hum jaldi aapko access de denge._ 🙏",
        parse_mode="Markdown"
    )

    # Owner ko notification
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=(
            f"🔔 *NEW PAYMENT RECEIVED!*\n\n"
            f"👤 Name: {user.full_name}\n"
            f"🆔 User ID: `{user.id}`\n"
            f"📛 Username: @{user.username if user.username else 'N/A'}\n"
            f"⭐ Stars Paid: *{stars_paid}*\n"
            f"🧾 Charge ID: `{charge_id}`\n\n"
            f"👉 User ko channel access do!"
        ),
        parse_mode="Markdown"
    )

# ─── APP SETUP ────────────────────────────────────────────────────────────────
ptb_app = Application.builder().token(BOT_TOKEN).build()
ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(CallbackQueryHandler(button_handler))
ptb_app.add_handler(PreCheckoutQueryHandler(pre_checkout))
ptb_app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

# ─── WEBHOOK ROUTES ───────────────────────────────────────────────────────────
@flask_app.post(f"/webhook/{BOT_TOKEN}")
def webhook():
    import asyncio, json
    from telegram import Update
    data = request.get_json(force=True)
    update = Update.de_json(data, ptb_app.bot)
    asyncio.run(ptb_app.process_update(update))
    return "ok", 200

@flask_app.get("/")
def health():
    return "Bot is running! ✅", 200

# ─── STARTUP ──────────────────────────────────────────────────────────────────
import asyncio

async def setup_webhook():
    await ptb_app.initialize()
    webhook_endpoint = f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}"
    await ptb_app.bot.set_webhook(webhook_endpoint)
    logger.info(f"Webhook set: {webhook_endpoint}")

if __name__ == "__main__":
    asyncio.run(setup_webhook())
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host="0.0.0.0", port=port)
