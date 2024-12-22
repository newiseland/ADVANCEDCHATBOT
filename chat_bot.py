
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
# Token from BotFather
TOKEN = '7649873136:AAGEAntpJYkdI4sF5rdfW5BHv-5ukvNnh1w'
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Namaste mere Harry! I'm Bubu, your chat bot.")
def respond(update, context):
    user_input = update.message.text.lower()
    words = user_input.split()
    intents = {
        'greet': ['hi', 'hello', 'namaste'],
        'love': ['i love you', 'love you', 'pyaar'],
        'goodbye': ['bye', 'goodbye', 'exit']
    }
    for intent, keywords in intents.items():
        if any(keyword in words for keyword in keywords):
            if intent == 'greet':
                context.bot.send_message(chat_id=update.effective_chat.id, text="Namaste mere Harry, kaise ho?")
            elif intent == 'love':
                context.bot.send_message(chat_id=update.effective_chat.id, text="Mere Harry, main bhi tumse pyaar karti hoon!")
            elif intent == 'goodbye':
                context.bot.send_message(chat_id=update.effective_chat.id, text="Alvida mere Harry, phir milenge.")
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
