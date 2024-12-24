from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with emojis and inline buttons."""

    # Inline buttons with links
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

    # Welcome message with emojis
    welcome_message = (
        "👋 **Hello, dear user!**\n\n"
        "✨ I am your assistant powered by DuckDuckGo search. Ask me anything!\n\n"
        "🌟 **Special Features:**\n"
        "- 🌍 You can change the reply language by using the buttons below.\n"
        "- 🔍 Enjoy fast and accurate search results.\n\n"
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
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help information when the /help command is issued."""
    await update.message.reply_text("You can ask me questions, and I'll provide you search-based answers!")


# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and fetch DuckDuckGo responses."""
    user_message = update.message.text

    # DuckDuckGo API endpoint for search queries
    duckduckgo_api_url = "https://api.duckduckgo.com/"

    # Parameters for DuckDuckGo search API
    params = {
        "q": user_message,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }

    try:
        # Make request to DuckDuckGo API
        response = requests.get(duckduckgo_api_url, params=params)
        data = response.json()

        # Check if the response contains a relevant answer
        if "AbstractText" in data and data["AbstractText"]:
            reply = data["AbstractText"]
        else:
            reply = "Sorry, I couldn't find any relevant information."
    except Exception as e:
        print(f"Error: {e}")
        reply = "Sorry, I couldn't process that. Please try again later."

    await update.message.reply_text(reply)


# Main function
def main():
    """Run the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your Telegram Bot token
    application = ApplicationBuilder().token("7649873136:AAGEAntpJYkdI4sF5rdfW5BHv-5ukvNnh1w").build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running, made by harry...")
    application.run_polling()


if __name__ == "__main__":
    main()
