import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pymongo import MongoClient

# MongoDB URI for connecting to the database
MONGO_URI = "mongodb://localhost:27017/"  # Replace this with your MongoDB URI if needed
DB_NAME = "telegram_bot_db"  # Database name
COLLECTION_NAME = "auto_replies"  # Collection name for storing auto-replies

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
auto_reply_collection = db[COLLECTION_NAME]  # MongoDB collection for storing auto-replies

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
        "✨ I am your assistant powered by MongoDB-based auto-reply. Ask me anything!\n\n"
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

# Command: Help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message with inline buttons for language options, back to start, and add to group."""
    keyboard = [
        [
            InlineKeyboardButton("🌍 Language", callback_data="language"),
            InlineKeyboardButton("🔙 Back to Start", callback_data="back_to_start"),
        ],
        [
            InlineKeyboardButton("➕ Add to Your Group", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    help_message = (
        "👋 **Welcome to Help Section!**\n\n"
        "I'm here to assist you with answers to your questions. You can:\n\n"
        "- 🌍 Choose a language for the replies.\n"
        "- 🔙 Go back to the start message.\n"
        "- ➕ Add me to your group.\n\n"
        "Feel free to ask any questions, and I'll try to help!"
    )

    await update.message.reply_text(
        help_message,
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

# Callback Query Handler for Inline Button Actions
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks for language selection, back to start, and adding to group."""
    query = update.callback_query
    data = query.data

    if data == "language":
        # You can modify this to provide a list of language options
        await query.answer("Language selection is not yet available!")
        return

    elif data == "back_to_start":
        await start(update, context)  # Go back to the start message

    await query.answer()

# Main function
def main():
    # Telegram bot token
    application = ApplicationBuilder().token("YOUR_BOT_API_KEY").build()  # Replace with your bot's token

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))  # Add help command

    # Message handler for auto-reply
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    # Callback Query handler
    application.add_handler(CallbackQueryHandler(button))

    print("Bot is running... Use /start to test it!")
    application.run_polling()

if __name__ == "__main__":
    main()
