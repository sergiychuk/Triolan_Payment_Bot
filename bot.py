# -*- coding: utf-8 -*-
import telebot
from telebot import types

token = '1775386822:AAElY-QwJK4Z5vR1FtvnLYP_lzhzZIZczo8'

bot = telebot.TeleBot(token, parse_mode='HTML')


@bot.message_handler(content_types=["text"])
def text_message_handler(message):
    bot.reply_to(message, 'Text: ' + message.text)


bot.polling()
