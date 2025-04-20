import telebot

# Your Bot Token
TOKEN = "8071923351:AAFEC7q-a4CWk5393T3Jm7JzO4oEOxk0KgI"

# Your Admin Group ID
ADMIN_GROUP_ID = -1002353507451

# Create bot
bot = telebot.TeleBot(TOKEN)

# Memory for simple access control (later replace with database)
paid_users = []

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in paid_users:
        bot.send_message(
            message.chat.id,
            "🎉 Welcome to Qi AI Awards!\n\nTo participate, please pay 50 Telegram Stars. Payment will be activated soon.\n\nFor now, please wait until registration opens."
        )
    else:
        bot.send_message(message.chat.id, "✅ You are registered! Send your AI-generated artwork now.")

# Receive Artwork
@bot.message_handler(content_types=['photo'])
def receive_artwork(message):
    user_id = message.from_user.id
    if user_id in paid_users:
        bot.forward_message(ADMIN_GROUP_ID, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "🖼️ Artwork received! Now send your AI generation proof (link or screenshot).")
    else:
        bot.send_message(message.chat.id, "⛔ You need to pay first!")

# Receive Proof (text link or screenshot document)
@bot.message_handler(content_types=['text', 'document'])
def receive_proof(message):
    user_id = message.from_user.id
    if user_id in paid_users:
        bot.forward_message(ADMIN_GROUP_ID, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "✅ Submission complete! Thank you.")
    else:
        bot.send_message(message.chat.id, "⛔ You need to pay first!")

# Run bot
bot.polling()
