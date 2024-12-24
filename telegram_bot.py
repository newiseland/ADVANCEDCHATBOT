import openai
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Set up OpenAI API key
openai.api_key = ("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")

# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I am your ChatGPT-powered assistant. Ask me anything!")

# Command: Help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help information when the /help command is issued."""
    await update.message.reply_text("You can ask me questions, and I'll try my best to answer them!")

# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and fetch ChatGPT responses."""
    user_message = update.message.text
    try:
        # Fetch response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
        )
        reply = response["choices"][0]["message"]["content"].strip()
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
    print("Bot is running made by harry...")
    application.run_polling()

if __name__ == "__main__":
    main()
