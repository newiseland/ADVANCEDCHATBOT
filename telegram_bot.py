import openai
import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Set up OpenAI API key (if you want to use OpenAI)
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
    print("Bot is running made by harry...")
    application.run_polling()

if __name__ == "__main__":
    main()
