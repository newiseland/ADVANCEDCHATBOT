import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
        "✨ I am your assistant powered by DuckDuckGo search. Ask me anything!\n\n"
        "🌟 **Special Features:**\n"
        "- 🌍 Change the reply language using the buttons below.\n"
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

def main():
    application = ApplicationBuilder().token("7649873136:AAGgVobroAHZMV7_1gGVNjeUJ_M78oq6vik").build()
    application.add_handler(CommandHandler("start", start))
    print("Bot is running... Use /start to test it!")
    application.run_polling()

if __name__ == "__main__":
    main()
