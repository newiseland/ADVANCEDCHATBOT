import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pymongo import MongoClient

# MongoDB URI for connecting to the database
MONGO_URI = "mongodb+srv://harryashutosh729:harryashutosh729@harry2.xykka.mongodb.net/?retryWrites=true&w=majority&appName=harry2"  # Replace this with your MongoDB URI if needed
DB_NAME = "telegram_bot_db"  # Database name
COLLECTION_NAME = "auto_replies"  # Collection name for storing auto-replies

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
auto_reply_collection = db[COLLECTION_NAME]  # MongoDB collection for storing auto-replies

# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message and a temporary sticker."""
    bot_username = context.bot.username  # Get the bot's username
    creator_username = "@creator_username"  # Replace with the actual creator's username

    # React with an emoji
    await update.message.reply_text("💗")

    # Send a sticker using the correct file_id
    sticker_file_id = "CAACAgQAAxkBAAEQ245ljYcpjiUzNlnqZayXwYGXQdQUYgAC2Q8AAnsbSFJTlxo-p_AUAAEzBA"
    sticker_message = await update.message.reply_sticker(sticker=sticker_file_id)

    # Wait for 5 seconds before deleting the sticker message
    await asyncio.sleep(5)
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=sticker_message.message_id)

    # Inline buttons
    keyboard = [
        [
            InlineKeyboardButton("👤 Owner", url="https://t.me/SANATANI_BACHA"),
            InlineKeyboardButton("📢 Support Channel", url="https://t.me/TG_NAME_STYLE"),
        ],
        [
            InlineKeyboardButton("💬 Support Group", url="https://t.me/TG_NAME_STYLE"),
            InlineKeyboardButton("🌐 Network", url="https://t.me/TG_NAME_STYLE"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Welcome message
    welcome_message = (
        f"👋 **Hello, {update.effective_user.first_name}!**\n\n"
        f"✨ I am your @{bot_username} powered by @SANATANI_BACHA, auto-reply bot. Ask me anything!\n\n"
        "🌟 **Special Features:**\n"
        "- 🌍 Change the reply language using the buttons below.\n"
        "- 🔍 Enjoy fast and accurate responses.\n\n"
        "💬 Feel free to explore and interact with me!\n\n"
        f"🔗 **Connect with us:** Use the buttons below to contact my owner or visit support resources.\n\n"
        f"**Created by @SANATANI_BACHA**\n\n"
        "**Thank you for starting me! 🎉**"
    )

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Auto-reply function
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto-reply to user messages based on MongoDB data."""
    user_message = update.message.text.lower()

    # Query MongoDB for a matching question
    result = auto_reply_collection.find_one({"question": user_message})

    if result:
        bot_response = result["response"]
    else:
        bot_response = "Sorry, I don't have an answer for that right now."

    # Send the response to the user
    await update.message.reply_text(bot_response)

# Main function
def main():
    # Telegram bot token
    application = ApplicationBuilder().token("7649873136:AAGgVobroAHZMV7_1gGVNjeUJ_M78oq6vik").build()  # Replace with your bot's token

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Message handler for auto-reply
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("Bot is running... Use /start to test it!")
    application.run_polling()

if __name__ == "__main__":
    main()
