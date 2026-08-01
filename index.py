import telebot

# Bot tokeningiz va o'zingizning Chat ID ingiz
TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 123456789  # Bu yerga o'zingizning Telegram chat_id ingizni yozasiz

bot = telebot.TeleBot(TOKEN)

# /start buyrug'i uchun
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.chat.id
    
    if user_id == ADMIN_ID:
        bot.reply_to(message, "Xush kelibsiz, Admin!")
    else:
        bot.reply_to(message, "Salom! Istalgan xabaringizni yuboring, adminga yetkazaman.")

# Barcha kelgan xabarlarni tutib olish
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.chat.id
    
    # Agar xabar Admindan BOSHQA odamdan kelgan bo'lsa
    if user_id != ADMIN_ID:
        # 1-usul: Xabarni o'zini sizga Forward (uzatish) qilish
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        
        # Foydalanuvchiga javob qaytarish
        bot.reply_to(message, "✅ Xabaringiz adminga yetkazildi!")
    else:
        # Agar admin xabar yozgan bo'lsa
        bot.reply_to(message, "Siz adminsiz. Boshqa foydalanuvchilar yozsa, xabarlari shu yerga keladi.")

bot.polling(none_stop=True)