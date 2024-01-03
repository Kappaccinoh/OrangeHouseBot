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

# api_url = 'https://laundrobot-api.onrender.com'
api_url = 'http://localhost:4000'

load_dotenv()
BOT_TOKEN = os.environ['BOT_TOKEN']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Bot Admin Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = \
        'HELLOO THEREE! My name is Soyaya, I am the mascot for Orange House! NICE TO MEET EVERYONE!\n\n' \
        'How may I assist yall today?' \
        'Type in /help for my full list of commands.'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = \
        '/create - Allows you to create a poll in which people can join\n\n' \


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
async def getpoll(update: Update, context: ContextTypes.DEFAULT_TYPE):

    json_body = {
        "chatid": update.message.chat_id,
    }

    r = requests.get(
        url=f'{api_url}/poll',
        json=json_body
    )

    title = requests.get(
        url=f'{api_url}/poll/getTitle',
        json=json_body
    )

    # Iterating and Formatting Database Values
    data = r.json()
    title = title.json()
    messageString = title[0]['polltitle'] + '\n\n'
    for d in data:
        name = d['name']
        room = d['room']
        telehandle = d['telehandle']
        sentence = f'{name} {room} @{telehandle}\n'
        messageString += sentence

    if r.status_code != requests.codes.ok:
        message = f'Error, no existing polls found'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        message = messageString
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='Enter the title of your Poll')
    
    return CREATEPOLL

async def createpoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = update.message.text
    chatid = update.message.chat_id

    json_body = {
        "chatid": chatid,
        "polltitle": title
    }

    # Sending POST HTTP Request
    r = requests.post(
        url=f'{api_url}/poll/create', 
        json=json_body
    )

    if r.status_code != requests.codes.ok:
        message = f'Error, poll already exists in this chat - {json_body["polltitle"]}, please type /delete to delete the existing poll, or type /join to join the existing poll'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        message = f'Poll Successfully Created - {json_body["polltitle"]}\n\n' \
            'type /join to join the poll'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    return ConversationHandler.END



async def deletepoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chatid = update.message.chat_id

    print(chatid)
    
    json_body = {
        "chatid": chatid,
    }

    # Sending GET HTTP Request
    r = requests.delete(
        url=f'{api_url}/poll/delete', 
        json=json_body
    )

    if r.status_code != requests.codes.ok:
        message = f'Error, no currently available polls'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        message = f'Poll Deleted Successfully - type /create to create a new poll'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    return ConversationHandler.END

async def getName(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='Enter your Name')
    
    return GETROOM

async def getRoom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['Name'] = update.message.text
    await update.message.reply_text(text='Enter your Room Number')
    
    return JOINPOLL

async def joinpoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Processing Room Format
    room = update.message.text
    if room.startswith('#'):
        room = room
    else:
        # Add # in front of the string
        room = '#' + room

    chatid = update.message.chat_id
    user = update.message.from_user
    user_handle = user['username']
        
    json_body = {
        "name": context.user_data.get('Name'),
        "room": room,
        "telehandle": user_handle,
        "chatid": chatid,
    }

    # Sending POST HTTP Request
    r = requests.post(
        url=f'{api_url}/poll/join', 
        json=json_body
    )

    if r.status_code != requests.codes.ok:
        message = f'Error, no currently available polls, type /create to create a new poll'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    else:
        message = f'Poll Joined Successfully'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        await getpoll(update, context)

    return ConversationHandler.END





# Main Driver Code

# Various State Numeration
CREATEPOLL = 1
GETROOM = 2
JOINPOLL = 3
GETPOLL = 4

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    getpoll_handler = CommandHandler("getpoll", getpoll)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("create", poll),
            CommandHandler("delete", deletepoll),
            CommandHandler("join", getName),
            CommandHandler("get", getpoll)
        ],
        states={
            CREATEPOLL: [MessageHandler(filters.TEXT, createpoll)],
            GETROOM: [MessageHandler(filters.TEXT, getRoom)],
            JOINPOLL: [MessageHandler(filters.TEXT, joinpoll)],
            GETPOLL: [MessageHandler(filters.TEXT, getpoll)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)
    application.add_handler(getpoll_handler)

    application.run_polling()
    
