# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token, parse_mode='HTML')

isDebug = config.debug_mode

bot_commands = ['start', 'help', 'print_phone', 'print_token', 'print_account', 'print_service_status']


@bot.message_handler(commands=['start'])
def command_start(message):
    set_chat_id(message)

    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) # , input_field_placeholder='FEZZZ')
    reply_keyboard.row('Мої рахунки', 'Сплатити')

    bot.send_message(config.cid, 'Привіти  <b>' + message.from_user.first_name + '</b>!', reply_markup=reply_keyboard)


@bot.message_handler(commands=['help'])
def command_help(message):
    set_chat_id(message)
    out_msg_text = 'Команди керування ботом:\n'
    for command in bot_commands:
        out_msg_text += '/' + command + '\n'
    bot.send_message(config.cid, out_msg_text)


@bot.message_handler(commands=['print_token'])
def command_print_token(message):
    set_chat_id(message)
    bot.send_message(config.cid, 'Token: <code>' + config.token + '</code>')


'''@bot.message_handler(commands=['print_phone'])
def command_print_phone(message):
    set_chat_id(message)
    bot.send_message(config.cid, 'Phone: <b>+' + config.account_phone + '</b>')


@bot.message_handler(commands=['print_account'])
def command_print_account(message):
    set_chat_id(message)
    bot.send_message(config.cid, 'Номер особового рахунку: <b>' + str(config.account) + '</b>')


@bot.message_handler(commands=['print_service_status'])
def command_print_service_status(message):
    set_chat_id(message)
    if config.service_status:
        bot.send_message(config.cid, 'Статус послуги: <i>увімкнена</i>')
    else:
        bot.send_message(config.cid, 'Статус послуги: <i>вимкнена</i>')'''


@bot.message_handler(content_types=["text"])
def text_message_handler(message):
    set_chat_id(message)
    msg_txt = message.text
    # bot.reply_to(message, 'Text: ' + message.text)
    if msg_txt == 'Сплатити':
        out_msg_text = '<a href="https://triolan.name">Triolan.NET</a>: ' + str(config.account) + '\n'
        out_msg_text += 'Послуга '
        if config.service_status:
            out_msg_text += 'увімкнена\n'
        else:
            out_msg_text += 'вимкнена\n'
        bot.send_message(config.cid, out_msg_text)


def set_chat_id(message):
    config.cid = message.chat.id
    if isDebug:
        print('Chat ID set to: ' + str(config.cid))


bot.polling()
