import os
import telebot
import re

BOT_TOKEN = os.environ.get('BOT_TOKEN')
# BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)
