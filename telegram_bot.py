import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with emojis, inline buttons, a personalized greeting, and a temporary sticker."""

    user = update.effective_user
    username = f"@{user.username}" if user.username else user.first_name

    # React with an emoji 💗
    await update.message.reply_text("💗")

    # Send a sticker (replace 'sticker_file_id' with an actual file ID or upload a sticker file)
    sticker_message = await update.message.reply_sticker("CAACAgUAAxkBAAEFMY1kM3hrwMj9_6MK6k2B6KfBJmhKpwACRQADkUoFG7UXzHLAlSzoLwQ")

    # Wait for 5 seconds before deleting the sticker message
    await asyncio.sleep(5)
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=sticker_message.message_id)

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

    # Welcome message with emojis and personalized greeting
    welcome_message = (
        f"👋 **Hello, {username}!**\n\n"
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


# Main function
def main():
    """Run the bot."""
    application = ApplicationBuilder().token("7649873136:AAGEAntpJYkdI4sF5rdfW5BHv-5ukvNnh1w").build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    print("Bot is running, made by harry...")
    application.run_polling()


if __name__ == "__main__":
    main()
