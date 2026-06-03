import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    PreCheckoutQueryHandler, filters, ContextTypes
)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN   = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
OWNER_ID    = int(os.environ.get("OWNER_ID", "8226637107"))
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", ""@Jatxchatbot")  # aapka username
STARS_AMOUNT = 100  # 100 Telegram Stars

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── /start COMMAND ──────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("⭐ Buy Material - 100 Stars (₹200)", callback_data="buy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        f"🎯 *Exclusive Study Material*\n\n"
        f"📦 Isme aapko premium material milega.\n\n"
        f"💰 *Price:* 100 ⭐ Telegram Stars (≈ ₹200)\n\n"
        f"Niche button dabao aur payment karo! ✅",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ─── BUTTON CALLBACK ─────────────────────────────────────────────────────────
from telegram.ext import CallbackQueryHandler

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="📚 Premium Study Material",
            description="Ek baar payment ke baad aapko exclusive material ka access milega.",
            payload="material_purchase",
            currency="XTR",           # XTR = Telegram Stars
            prices=[LabeledPrice("Premium Material", STARS_AMOUNT)],
            provider_token=""          # Stars ke liye empty string
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

    stars_paid = payment.total_amount  # Stars mein amount
    charge_id  = payment.telegram_payment_charge_id

    # ── User ko confirmation ──────────────────────────────────────────────────
    await update.message.reply_text(
        f"✅ *Payment Successful!*\n\n"
        f"Aapne *{stars_paid} ⭐ Stars* pay kar diye!\n\n"
        f"🔓 Access ke liye niche contact karo:\n"
        f"👉 {OWNER_USERNAME}\n\n"
        f"_Hum 1-2 ghante mein aapko access de denge._",
        parse_mode="Markdown"
    )

    # ── Owner ko notification ─────────────────────────────────────────────────
    user_info = (
        f"👤 Name: {user.full_name}\n"
        f"🆔 User ID: `{user.id}`\n"
        f"📛 Username: @{user.username if user.username else 'N/A'}\n"
    )

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=(
            f"🔔 *NEW PAYMENT RECEIVED!*\n\n"
            f"{user_info}"
            f"⭐ Stars Paid: *{stars_paid}*\n"
            f"🧾 Charge ID: `{charge_id}`\n\n"
            f"👉 Jaldi user ko channel access do!"
        ),
        parse_mode="Markdown"
    )

    logger.info(f"Payment received from {user.id} ({user.username}) - {stars_paid} stars")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    logger.info("🤖 Bot chal raha hai...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
