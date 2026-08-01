"""
Telegram bot: foydalanuvchi yuborgan HAR QANDAY xabarni
(o'zgarishsiz - matn, rasm, video, ovozli xabar, fayl va h.k.)
belgilangan ADMIN_CHAT_ID ga forward qiladi.

Foydalanuvchiga esa har safar natija haqida javob yoziladi:
  - "✅ Xabaringiz yuborildi"
  - "❌ Xabaringiz yuborilmadi"

O'RNATISH:
  pip install python-telegram-bot --upgrade

ISHGA TUSHIRISH:
  python3 forward_bot.py
"""

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ====== SOZLAMALAR ======
BOT_TOKEN = "8710081589:AAFiYx4haIpy2nI2MkMjcHddOmmhfKhwbMQ"
ADMIN_CHAT_ID = 812796533
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Menga istalgan xabar, rasm, video yoki faylni "
        "yuboring — u to'g'ridan-to'g'ri yetkaziladi."
    )


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message is None:
        return

    try:
        # forward_message xabarni O'ZGARTIRMAY (matn, media, fayl - har qanday turi)
        # asl ko'rinishida ADMIN_CHAT_ID ga yuboradi.
        await context.bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id,
        )
        await message.reply_text("✅ Xabaringiz yuborildi")
    except Exception as e:
        logger.error(f"Xabarni forward qilishda xatolik: {e}")
        await message.reply_text("❌ Xabaringiz yuborilmadi")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # /start dan boshqa har qanday xabar turini ushlab, forward qiladi
    app.add_handler(MessageHandler(~filters.COMMAND, forward_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
