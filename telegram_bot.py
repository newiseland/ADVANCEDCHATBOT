import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Set your OpenAI API key
openai.api_key = "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"

# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I am ChatGPT-powered bot. How can I help you today?")

# Command: Help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help information when the /help command is issued."""
    await update.message.reply_text("You can ask me anything, and I'll try my best to assist you!")

# ChatGPT Integration
async def chat_with_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and return ChatGPT responses."""
    user_message = update.message.text
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
        )
        # Extract GPT's reply
        gpt_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(gpt_reply)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Sorry, I couldn't process that. Please try again later.")

# Main Function
def main():
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your bot's token
    application = ApplicationBuilder().token("7649873136:AAGEAntpJYkdI4sF5rdfW5BHv-5ukvNnh1w").build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Message Handler (ChatGPT Integration)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    # Run the bot
    print("ChatGPT Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
