from dotenv import load_dotenv
import os
import logging
import telegram
from telegram import *
from telegram.ext import *
import requests
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

api_url = 'https://laundrobot-api.onrender.com'
api_url = 'http://localhost:4000'

load_dotenv()
BOT_TOKEN = os.environ['BOT_TOKEN']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot Admin Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton('Poll')],
        [KeyboardButton('Help')]
    ]
    text = \
        'HELLOO THEREE! My name is Soyaya, I am the mascot for Orange House! NICE TO MEET EVERYONE!\n\n' \
        'How may I assist yall today?' \
        'Type in /help for my full list of commands.'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=ReplyKeyboardMarkup(buttons))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton('Poll')],
        [KeyboardButton('Help')]
    ]

    text = \
        'Poll - Allows you to create a poll in which people can join'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=ReplyKeyboardMarkup(buttons))

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# Function which responds to KeyboardMarkup Options, triggers the specific set of the bot's capabilities
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text

    if text == 'Create Poll':
        await poll(update, context)
    elif text == 'Help':
        await help(update, context)
    else:
        await start(update, context)


# Polling Functions
async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton('Create Poll')],
        [KeyboardButton('Join')],
        [KeyboardButton('Remove')]
        [KeyboardButton('Delete Poll')]
        [KeyboardButton('Help')]
    ]

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=ReplyKeyboardMarkup(buttons))

# Main Driver Code
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
    
