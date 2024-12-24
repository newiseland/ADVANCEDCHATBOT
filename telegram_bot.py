from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram import Update
from telegram import filters  # Updated filters import

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I am your bot. How can I assist you?")

# Function to handle regular messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    if "hello" in user_message:
        update.message.reply_text("Hi there! How can I help you?")
    elif "bye" in user_message:
        update.message.reply_text("Goodbye! Have a great day!")
    else:
        update.message.reply_text("I'm not sure how to respond to that.")

# Main function to start the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = "7649873136:AAGEAntpJYkdI4sF5rdfW5BHv-5ukvNnh1w"

    # Create the Updater and pass the bot token
    updater = Updater(token=bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handler for /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Message handler for all text messages
    dispatcher.add
