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

CREATEPOLL = range(1)

# Bot Admin Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = \
        'HELLOO THEREE! My name is Soyaya, I am the mascot for Orange House! NICE TO MEET EVERYONE!\n\n' \
        'How may I assist yall today?' \
        'Type in /help for my full list of commands.'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = \
        '/poll - Allows you to create a poll in which people can join'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


# Polling Functions
async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='Enter the title of your Poll')
    
    return CREATEPOLL

async def createpoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = update.message.text

    print(title)

    # send json data 

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Poll Successfully Created")
    
    return ConversationHandler.END


async def deletepoll(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    text = message.text

    await context.bot.send_message(chat_id=update.effective_chat.id, text="deletepoll")



# Main Driver Code
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("poll", poll)],
        states={
            CREATEPOLL: [MessageHandler(filters.TEXT, createpoll)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
    
