import os
import telebot
import re

BOT_TOKEN = os.environ.get('BOT_TOKEN')
# BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)


# Global Constants
list_exists = False

# original list is stored as such - all variables are strings
# [
#   [name, room_number, handle]
# ]
title = ""
list_of_names = []


# Helper Functions
def extract_arg(arg):
    return arg.split()

def extract_title(arg):
    return arg[8:]

def clear_list():
    list_of_names = []

def print_message():
    global title
    message = title + "\n"
    for row in list_of_names:
        message = message + row[0] + " " + row[1] + " " + row[2] + "\n"
    return message

def update_message(name, room_number, username):
    global list_of_names
    flag = True
    for entry in list_of_names:
        if "@" + username == entry[2]:
            entry[0] = name
            entry[1] = room_number
            flag = False
            break

    if flag:
        detail = [name, room_number, "@" + username]
        list_of_names.append(detail)

def remove_name(username):
    global list_of_names
    for entry in list_of_names:
        if "@" + username == entry[2]:
            list_of_names.remove(entry)
            return True
    return False


# Bot Commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "HELLOO THEREE! My name is Soyaya, I am the mascot for Orange House! NICE TO MEET EVERYONE!\n\nHow may I assist yall today? Type in /help for my full list of commands.")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 
        "/create <title> - Creates a new and empty list\n" +
        "/join <your_name> <room_number> - Joins and or updates the current list (type /join again to override your previous entry)\n" +
        "/remove - Removes your current entry\n" +
        "/end - Deletes the current list of names"
    )


@bot.message_handler(commands=['create'])
def create_new_list(message):
    global list_exists
    global title
    if not list_exists:
        try:
            ls_title = extract_arg(message.text)[1]
        except:
            bot.reply_to(message, "Your list needs a title! - Missing parameters, type '/create <title>'")
        else:        
            title = extract_title(message.text)
            list_exists = True
            # bot.send_message(message.chat.id, title)
            bot.send_message(message.chat.id, "To add an item to the list, type '/join <your_name> <room_number>'")
    else:
        bot.reply_to(message, "There is an ongoing list already, type /end if you wish to terminate the current list, if not /join ")


@bot.message_handler(commands=['join'])
def send_join_error(message):
    global list_exists
    global list_of_names
    if list_exists:
        try:
            name = extract_arg(message.text)[1]
            room_number = extract_arg(message.text)[2]
        except:
            bot.reply_to(message, "Missing parameters. type '/join <your_name> <room_number>'")
        else:
            # check if room_number has # or is not an integer
            # case 1: /join jiawei #21-114
            # case 2: /join jia wei #21-114
            # case 3: /join jiawei 21-114
            if re.search('[a-zA-Z]', room_number) != None:
                bot.reply_to(message, "Invalid Room Number, I think your name has a space in it, please remove it. type '/join <your_name> <room_number>'")
            else:
                if re.search('#', room_number) != None:
                    room_number = room_number[1:]
                room_number = "#" + room_number
                username = message.from_user.username
                update_message(name, room_number, username)
                final_list = print_message()
                bot.send_message(message.chat.id, final_list)
    else:
        bot.reply_to(message, "The list does not exist yet, type '/create <title>' to create a new list")

@bot.message_handler(commands=['remove'])
def remove_entry(message):
    global list_exists
    global list_of_names
    if list_exists:
        remove_name(message.from_user.username)
        bot.reply_to(message, "Removed successfully, type '/join <your_name> <room_number>' to write a new entry")
        final_list = print_message()
        bot.send_message(message.chat.id, final_list)

    else:
        bot.reply_to(message, "The list does not exist yet, type '/create <title>' to create a new list")


@bot.message_handler(commands=['end'])
def delete_list(message):
    global list_exists
    global list_of_names
    global title
    if list_exists:
        list_exists = False
        list_of_names=[]
        title = ""
        bot.reply_to(message, "List deleted successfully, type '/create <title>' to create a new list")

    else:
        bot.reply_to(message, "The list does not exist yet, type '/create <title>' to create a new list")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "I'm sorry I don't understand - Invalid command, type /help for a full list of commands.")

bot.infinity_polling()
