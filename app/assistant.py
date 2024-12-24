import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set your OpenAI API key and Telegram bot token
OPENAI_API_KEY = "<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>"
TELEGRAM_BOT_TOKEN = "7649873136:AAGEAntpJYkdI4sF5rdfW5BHv-5ukvNnh1w"

# Configure OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to get a response from OpenAI GPT model
def chat_with_gpt(prompt):
    """Send a prompt to OpenAI API and get the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use gpt-3.5-turbo if gpt-4 is unavailable
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text("Hello! I am your assistant. Ask me anything!")

# Message handler for user queries
def handle_message(update: Update, context: CallbackContext) -> None:
    """Process user messages and respond with OpenAI's GPT."""
    user_message = update.message.text
    update.message.reply_text("Thinking...")
    try:
        # Get GPT response
        response = chat_with_gpt(user_message)
        update.message.reply_text(response)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Main function to run the bot
def main():
    """Start the Telegram bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Run the bot
if __name__ == "__main__":
    main()
