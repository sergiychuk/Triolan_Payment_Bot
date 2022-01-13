# -*- coding: utf-8 -*-
# region ──────────╼[ IMPORT ]╾──────────
import telebot
from telebot import *
from telebot.types import *

from Config import *
from Settings import settings_handler as settings
from Keyboard import keyboard
from Data import data as bot_data
# endregion

bot = TeleBot(Token, parse_mode='HTML')


# payment_method_variant = ''
# payment_amount = ''
#
# bot_commands = ['start', 'help', 'print_phone', 'print_token', 'print_account', 'print_service_status']

# region ──────────╼[ BOT COMMANDS ]╾──────────
@bot.message_handler(commands=['start'])
def command_start(message):
    # link_text = f'<a href="{bot_data.get_payment_link("Portmone", 40)}">inline URL</a>'
    chat_id = message.from_user.id
    ResetBot(chat_id)
    bot.send_message(chat_id=chat_id,
                     text=GenTextMainMenu(),
                     disable_web_page_preview=True,
                     reply_markup=keyboard.main_menu)

@bot.message_handler(commands=['debug_mode'])
def command_debug_mode(message):
    chat_id = message.from_user.id
    settings.debug_mode = not settings.debug_mode
    out_text = f'<i>Debug Mode: '
    out_text += f'<b>ON</b></i>' if settings.debug_mode else '<b>OFF</b></i>'
    bot.send_message(chat_id=chat_id, text=out_text)

@bot.message_handler(commands=['bot_state'])
def command_bot_state(message):
    chat_id = message.from_user.id
    settings.debug_mode = not settings.debug_mode
    out_text = f'<i>Bot State: <b>{bot.get_state(chat_id)}</b></i>'
    bot.send_message(chat_id=chat_id, text=out_text)
# endregion


# region ──────────╼[ BOT FUNCTIONS ]╾──────────
# region ───[Generate text for main menu]───
def GenTextMainMenu():
    text = f'<i>Номер договору:</i> <code>{bot_data.account_id}</code>\n' \
           f'<i>Платіжна система:</i> <code>{bot_data.payment_service}</code>\n' \
           f'<i>Кількіть днів:</i> <b><i>{bot_data.payment_days_amount}</i></b>\n' \
           f'<i>Сума платежу:</i> <b><i>{bot_data.payment_money_amount} грн</i></b>\n'
    return text
# endregion
# region ───[Generate text for changing payment system]───
def GenTextPaymentSystemMenu():
    text = f'<i>Обрана платіжна система:</i> <b>{bot_data.payment_service}</b>\n'
    transfer_fee = round(bot_data.payment_money_amount * 0.2, 1)
    if bot_data.payment_money_amount > 0:
        text += f'<code>></code> <i>комісія <b>2%</b> (~<b>{transfer_fee}</b> грн), не менше <b>2</b> грн.</i>'

    return text
# endregion
# region ───[Generate text for changing days amount menu]───
def GenTextChangingDaysAmount():
    text = f'<i>Збільшення терміну дії послуги на:</i> <i><b><u>{bot_data.payment_days_amount}</u></b> днів.</i>\n'
    if bot_data.payment_days_amount > 0:
        text += f'<code>></code> <i>вартість платежу: <b><i>{bot_data.payment_money_amount}</i></b> грн.</i>'
    return text
# endregion
# region ───[Generate text for changing money amount menu]───
def GenTextChangingMoneyAmount():
    text = f'<i>Сума платежу:</i> <b><i><u>{bot_data.payment_money_amount}</u> грн</i></b>\n'
    if bot_data.payment_money_amount > 0:
        # text += f'<tg-spoiler><code>></code> <i>продовження терміну дії послуги на <b><i><u>{bot_data.payment_days_amount}</u></i></b> днів.</i></tg-spoiler>'
        text += f'<code>></code> <i>продовження терміну дії послуги на <b><i><u>{bot_data.payment_days_amount}</u></i></b> днів.</i>'
    return text
# endregion
# region ───[Generate text for changing contract id menu]───
def GenTextChangingContractId():
    text = f'<i>Номер договору:</i> <b><i><u>{bot_data.account_id}</u>.</i></b>\n'
    return text
# endregion
# region ───[Generate text for generating final payment link menu]───
def GenTextPaymentLink():
    text = f'<b><u>Оплата послуги доступу в інтернет:</u></b>\n' \
           f'<code>></code> <i>номер особового рахунку:</i> <code>{bot_data.account_id}</code>\n' \
           f'<code>></code> <i>сума платежу:</i> <code>{bot_data.payment_money_amount}</code>\n' \
           f'<code>></code> <i>продовження терміну дії послуги:</i> <code>{bot_data.payment_days_amount}</code> <i>днів.</i>\n'
    return text
# endregion

# region ───[Reset all bot data]───
def ResetBot(chat_id):
    # Reset bot state
    if bot.get_state(chat_id):
        bot.delete_state(chat_id)
# endregion

# endregion

# region ──────────╼[ CALLBACK HANDLER ]╾──────────
@bot.callback_query_handler(func=lambda call: True)  # Обработка всех callback событий
def callback_query_handler(call):
    # region ──┨ VARIABLES ┠──
    chat_id = call.message.chat.id  # NOTE: ID чата от которого пришел callback
    # call_data = call.data[3:]  # NOTE: текст callback.data без "cb_" в начале
    # call_message = call.message                 # Сообщение от которого пришел callback
    call_message_id = call.message.message_id  # NOTE: ID сообщения от которого пришел callback
    # endregion

    # region ──┨ IF DEBUG MODE ON ┠──
    if settings.debug_mode:
        bot.answer_callback_query(callback_query_id=call.id, text=f'Callback data: {call.data}')
    # endregion

    # region ──┨ BUTTONS HANDLERS ┠──
    # region [ Button: Cahnge Days Amount ]
    if call.data == 'change days_amount':
        bot.set_state(chat_id, 'set_days_amount')  # Set bot state
        bot.edit_message_text(text=GenTextChangingDaysAmount(),
                              chat_id=chat_id,
                              message_id=call_message_id,
                              reply_markup=keyboard.days_amount_menu)
    # endregion
    # region [ Buttons: Days Amount Changing ]
    if call.data.split(' ')[0] == 'days_amount':
        if call.data.split(' ')[1] == 'increase':
            bot_data.payment_days_amount += 1
            bot.edit_message_text(text=GenTextChangingDaysAmount(),
                                  chat_id=chat_id,
                                  message_id=call_message_id,
                                  reply_markup=keyboard.days_amount_menu)

        if call.data.split(' ')[1] == 'decrease':
            if bot_data.payment_days_amount - 1 >= 0:
                bot_data.payment_days_amount -= 1
                bot.edit_message_text(text=GenTextChangingDaysAmount(),
                                      chat_id=chat_id,
                                      message_id=call_message_id,
                                      reply_markup=keyboard.days_amount_menu)
            else:
                bot_data.payment_days_amount = 0
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Кількість днів може бути цілим додатнім числом!',
                                          show_alert=True)
                bot.edit_message_text(text=GenTextChangingDaysAmount(),
                                      chat_id=chat_id,
                                      message_id=call_message_id,
                                      reply_markup=keyboard.days_amount_menu)

    if call.data.split(' ')[0] == 'set_days_amount':
        bot_data.payment_days_amount = int(call.data.split(' ')[1])
        bot.edit_message_text(text=GenTextChangingDaysAmount(),
                              chat_id=chat_id,
                              message_id=call_message_id,
                              reply_markup=keyboard.days_amount_menu)
    # endregion

    # region [ Buttons: Change Money Amount ]
    if call.data == 'change money_amount':
        bot.set_state(chat_id, 'set_money_amount')  # Set bot state
        bot.edit_message_text(text=GenTextChangingMoneyAmount(),
                              chat_id=chat_id,
                              message_id=call_message_id,
                              reply_markup=keyboard.money_amount_menu)
    # endregion
    # region [ Buttons: Money Amount Changing ]
    if call.data.split(' ')[0] == 'money_amount':
        if call.data.split(' ')[1] == 'increase':
            bot_data.payment_money_amount += 4
            bot.edit_message_text(text=GenTextChangingMoneyAmount(),
                                  chat_id=chat_id,
                                  message_id=call_message_id,
                                  reply_markup=keyboard.money_amount_menu)
        if call.data.split(' ')[1] == 'decrease':
            if bot_data.payment_money_amount - 4 >=0:
                bot_data.payment_money_amount -= 4
                bot.edit_message_text(text=GenTextChangingMoneyAmount(),
                                      chat_id=chat_id,
                                      message_id=call_message_id,
                                      reply_markup=keyboard.money_amount_menu)
            else:
                bot_data.payment_money_amount = 0
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Сума платежу може бути тільки цілим додатнім числом!',
                                          show_alert=True)
                bot.edit_message_text(text=GenTextChangingMoneyAmount(),
                                      chat_id=chat_id,
                                      message_id=call_message_id,
                                      reply_markup=keyboard.money_amount_menu)

    if call.data.split(' ')[0] == 'set_money_amount':
        bot_data.payment_money_amount = int(call.data.split(' ')[1])
        bot.edit_message_text(text=GenTextChangingMoneyAmount(),
                              chat_id=chat_id,
                              message_id=call_message_id,
                              reply_markup=keyboard.money_amount_menu)
    # endregion

    # region [ Buttons: Change Payment System ]
    if call.data == 'change payment_system':
        bot.edit_message_text(text=GenTextPaymentSystemMenu(),
                              chat_id=chat_id,
                              message_id=call_message_id,
                              reply_markup=keyboard.payment_system_menu)
    # endregion
    # region [ Buttons: Changing Payment System ]
    if call.data.split(' ')[0] == 'set_payment_system':
        bot_data.payment_service = call.data.split(' ')[1]
        bot.edit_message_text(text=GenTextPaymentSystemMenu(),
                              chat_id=chat_id,
                              message_id=call_message_id,
                              reply_markup=keyboard.payment_system_menu)
    # endregion

        # region [ Buttons: Changing Payment System ]
        if call.data.split(' ')[0] == 'set_payment_system':
            bot_data.payment_service = call.data.split(' ')[1]
            bot.edit_message_text(text=GenTextPaymentSystemMenu(),
                                  chat_id=chat_id,
                                  message_id=call_message_id,
                                  reply_markup=keyboard.payment_system_menu)
        # endregion
    # endregion

    # region [ Button: Contract ID) ]
    if call.data.split(' ')[0] == 'change':
        if call.data.split(' ')[1] == 'contract_id':
            bot.set_state(chat_id, 'set_contract_id')  # Set bot state
            bot.edit_message_text(text=GenTextChangingContractId(),
                                  chat_id=chat_id,
                                  message_id=call_message_id,
                                  reply_markup=keyboard.contract_id_menu)
    # endregion

    # region [ Button: Return to Main Main  ]
    if call.data.split(' ')[0] == 'return':
        if call.data.split(' ')[1] == 'main_menu':
            ResetBot(chat_id)
            bot.edit_message_text(text=GenTextMainMenu(),
                                  chat_id=chat_id,
                                  message_id=call_message_id,
                                  disable_web_page_preview=True,
                                  reply_markup=keyboard.main_menu)
    # endregion

    # region [ Button: Show payment link) ]
    if call.data.split(' ')[0] == 'show':
        if call.data.split(' ')[1] == 'payment_link':
            bot.send_message(chat_id=chat_id,
                             text=GenTextPaymentLink(),
                             reply_markup=keyboard.payment_link_menu)
    # endregion

# endregion

# region ──────────╼[ Handle messages by bot_state and message content_types ]╾──────────
# region ──────────┨ STATE: set_days_amount ┠──────────
@bot.message_handler(state="set_days_amount", content_types='text', is_digit=True)
def get_days_amount(message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id - 1)  # Delete previous message with changing days amount keyboard
    bot_data.payment_days_amount = int(message.text)
    bot.send_message(chat_id, GenTextChangingDaysAmount(), reply_markup=keyboard.days_amount_menu)

@bot.message_handler(state="set_days_amount", content_types='text', is_digit=False)
def get_incorrect_days_amount(message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id - 1)  # Delete previous message with changing days amount keyboard
    bot.reply_to(message=message,
                 text='<code>Кількість днів повинно бути цілим додатнім числом!</code>')
    bot.send_message(chat_id=chat_id,
                     text=GenTextChangingDaysAmount(),
                     reply_markup=keyboard.days_amount_menu)
# endregion
# region ──────────┨ STATE: set_money_amount ┠──────────
@bot.message_handler(state="set_money_amount", content_types='text', is_digit=True)
def get_money_amount(message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id - 1)  # Delete previous message with changing days amount keyboard
    bot_data._payment_money_amount = message.text

    bot.send_message(chat_id=chat_id,
                     text=GenTextChangingMoneyAmount(),
                     reply_markup=keyboard.money_amount_menu)

@bot.message_handler(state="set_money_amount", content_types='text', is_digit=False)
def get_incorrect_money_amount(message):
    chat_id = message.chat.id
    error_msg = bot.send_message(chat_id=chat_id,
                     text='<code>Сума платежу повинна бути цілим додатнім числом!</code>',
                     reply_to_message_id=message.message_id)
    bot.delete_message(chat_id, message.message_id - 1)  # Delete previous message with changing days amount keyboard
    bot.send_message(chat_id=chat_id,
                     text=GenTextChangingMoneyAmount(),
                     reply_markup=keyboard.money_amount_menu)
# endregion
# region ──────────┨ STATE: set_contract_id ┠──────────
@bot.message_handler(state="set_contract_id", content_types='text', is_digit=True)
def get_contract_id(message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id - 1)  # Delete previous message with changing days amount keyboard

    bot_data.account_id = int(message.text)

    bot.send_message(chat_id=chat_id,
                     text=GenTextChangingContractId(),
                     reply_markup=keyboard.contract_id_menu)

@bot.message_handler(state="set_contract_id", content_types='text', is_digit=False)
def get_incorrect_contract_id(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='<code>Номер особового рахунку має бути цілим додатнім числом!</code>',
                     reply_to_message_id=message.message_id)
    bot.delete_message(chat_id, message.message_id - 1)  # Delete previous message with changing days amount keyboard
    bot.send_message(chat_id=chat_id,
                     text=GenTextChangingContractId(),
                     reply_markup=keyboard.contract_id_menu)
# endregion

# endregion

# region ──────────╼[ BOT GENERAL FUNCTIONS ]╾──────────
# bot.set_update_listener(update_listener)
bot.add_custom_filter(custom_filters.StateFilter(bot))  # Добавление кастомных состояний бота
bot.add_custom_filter(custom_filters.IsDigitFilter())  # Фильтрация текста сообщения по цифре
bot.infinity_polling(timeout=0, skip_pending=True, long_polling_timeout=0)  # Запуск бота
# endregion
