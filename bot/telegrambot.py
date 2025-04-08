from dotenv import load_dotenv
import os
load_dotenv()
import telebot
key = os.environ['api']

API_TOKEN = key

bot = telebot.TeleBot(API_TOKEN)

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to YourBot! Type /info to get more information.")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Start the bot
bot.polling()