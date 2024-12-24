import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pymongo import MongoClient

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
DB_NAME = "telegram_bot_db"
COLLECTION_NAME = "chat_responses"
SETTINGS_COLLECTION = "chat_settings"

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]
settings_collection = db[SETTINGS_COLLECTION]

# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message and a temporary sticker."""
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
        "✨ I am your assistant powered by a custom MongoDB database. Ask me anything!\n\n"
        "🌟 **Special Features:**\n"
        "- 🌍 Change the reply language using the buttons below.\n"
        "- 🔍 Enjoy fast and accurate responses.\n\n"
        "💬 Feel free to explore and interact with me!\n\n"
        "🔗 **Connect with us:** Use the buttons below to contact my owner or visit support resources.\n\n"
        "**Thank you for starting me! 🎉**"
    )

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Command: Enable chatbot
async def enable_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enable chatbot for a group."""
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command can only be used in groups.")
        return

    chat_id = update.effective_chat.id

    # Remove chat from the disabled list in MongoDB
    settings_collection.delete_one({"chat_id": chat_id})
    await update.message.reply_text("Chatbot has been enabled for this group!")

# Command: Disable chatbot
async def disable_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Disable chatbot for a group."""
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command can only be used in groups.")
        return

    chat_id = update.effective_chat.id

    # Add chat to the disabled list in MongoDB
    if not settings_collection.find_one({"chat_id": chat_id}):
        settings_collection.insert_one({"chat_id": chat_id})
    await update.message.reply_text("Chatbot has been disabled for this group!")

# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to user messages based on MongoDB data."""
    chat_id = update.effective_chat.id

    # Check if chatbot is disabled for this chat
    if settings_collection.find_one({"chat_id": chat_id}):
        return  # Ignore messages if chatbot is disabled

    user_message = update.message.text

    # Query MongoDB for a response
    response = collection.find_one({"question": user_message})

    if response:
        # Reply with the stored answer
        reply = response.get("answer", "Sorry, I don't know the answer to that.")
    else:
        # Reply with a default message if no answer is found
        reply = "I don't know the answer to that yet. Please ask something else."

    await update.message.reply_text(reply)

def main():
    # Telegram bot token
    application = ApplicationBuilder().token("7649873136:AAGgVobroAHZMV7_1gGVNjeUJ_M78oq6vik").build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chatbot_on", enable_chatbot))
    application.add_handler(CommandHandler("chatbot_off", disable_chatbot))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running... Use /start to test it!")
    application.run_polling()

if __name__ == "__main__":
    main()
