import logging
from app import Update
from app.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# OpenAI API Key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7649873136:AAGEAntpJYkdI4sF5rdfW5BHv-5ukvNnh1w"

# Define system message (optional, guides bot behavior)
SYSTEM_MESSAGE = "You are an advanced AI assistant skilled in answering technical and general queries."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command.
    """
    await update.message.reply_text(
        "Hello! I'm your ChatGPT-powered bot. Ask me anything!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /help command.
    """
    await update.message.reply_text(
        "I am an AI bot powered by OpenAI's GPT model. Just type your question, and I'll respond!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle user messages and generate responses using OpenAI's GPT API.
    """
    user_message = update.message.text
    try:
        logging.info(f"Received message: {user_message}")
        
        # Call OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if "gpt-4" is unavailable
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        bot_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_reply)
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        await update.message.reply_text("I'm sorry, I encountered an error. Please try again later.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """
    Log the errors caused by updates.
    """
    logging.error(msg="Exception while handling an update:", exc_info=context.error)

def main():
    """
    Start the Telegram bot.
    """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    application.add_error_handler(error_handler)

    # Run the bot
    logging.info("Starting the bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
