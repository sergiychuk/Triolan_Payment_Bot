# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token, parse_mode='HTML')

isDebug = config.debug_mode

payment_method_variant = ''
payment_amount = ''

bot_commands = ['start', 'help', 'print_phone', 'print_token', 'print_account', 'print_service_status']


@bot.message_handler(commands=['start'])
def command_start(message, t = 0):
    set_chat_id(message)

    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) # , input_field_placeholder='FEZZZ')
    reply_keyboard.add('Сплатити')
    reply_keyboard.row( 'Мої рахунки', 'Налаштування')

    if t == 0:
        bot.send_message(config.cid, 'Привіти  <b>' + message.from_user.first_name + '</b>!')
    bot.send_message(config.cid, 'ГОЛОВНЕ МЕНЮ', reply_markup=reply_keyboard)


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

    if msg_txt == 'Сплатити':
        reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   input_field_placeholder='Вибери сервіс оплати')
        reply_keyboard.row('PrivatBank', 'Portmone', 'iPay')
        reply_keyboard.add('Повернутися')

        out_msg_text = '<b><a href="http://Triolan.net">Triolan.NET</a></b>: ' + str(config.account) + '\n'
        out_msg_text += get_service_status(config.service_status)
        out_msg_text += 'Сплачено по: <b>' + config.paid_until + '</b>'

        send = bot.send_message(config.cid, out_msg_text, reply_markup=reply_keyboard)
        bot.register_next_step_handler(send, chose_payment_service)

    elif msg_txt == 'Повернутися':
        command_start(message, 1)

    elif msg_txt == 'Мої рахунки':
        out_msg_text = 'Особові рахунки закріплені за телефоном: <b>' + str(config.account_phone) + '</b>'
        bot.send_message(config.cid, out_msg_text)
        out_msg_text = '<b><a href="https://Triolan.net">Triolan.NET</a></b>: ' + str(config.account) + '\n'
        out_msg_text += 'м.Ровно, Вячеслава Черновола улица, буд.51\n'
        out_msg_text += 'Сплачено по: ' + config.paid_until + '\n'
        out_msg_text += get_service_status(config.service_status)
        bot.send_message(config.cid, out_msg_text)

    elif msg_txt == 'Налаштування':
        out_msg_text = 'Меню Налаштувань'
        reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply_keyboard.row('Статус послуги', 'Кінцева дата')
        reply_keyboard.add('Повернутися')
        bot.send_message(config.cid, out_msg_text, reply_markup=reply_keyboard)

    elif msg_txt == 'Статус послуги':
        reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   input_field_placeholder='Вибери чи введи статус послуги')
        reply_keyboard.row('Увімкнути', 'Вимкнути')
        send = bot.send_message(config.cid, get_service_status(config.service_status), reply_markup=reply_keyboard)
        bot.register_next_step_handler(send, set_service_status)

    elif msg_txt == 'Кінцева дата':
        reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   input_field_placeholder='Дата дії послуги...')
        reply_keyboard.add('Повернутися')
        send = bot.send_message(config.cid, 'Сплачено по: ' + config.paid_until, reply_markup=reply_keyboard)
        bot.register_next_step_handler(send, set_paid_until_date)


def set_service_status(message):
    if message.text == 'Увімкнути':
        config.set_service_status(True)
    elif message.text == 'Вимкнути':
        config.set_service_status(False)
    bot.send_message(config.cid, get_service_status(config.service_status))
    command_start(message, 1)


def set_paid_until_date(message):
    if message.text != 'Повернутися':
        config.set_paid_until_date(message.text)
    command_start(message, 1)


def set_chat_id(message):
    config.cid = message.chat.id
    if isDebug:
        print('Chat ID set to: ' + str(config.cid))


def get_service_status(status):
    msg_text = 'Послуга <b>'
    if status:
        msg_text += 'увімкнена</b>\n'
    else:
        msg_text += 'вимкнена</b>\n'
    return msg_text


def chose_payment_service(message):
    global payment_method_variant
    payment_method_variant = message.text
    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               input_field_placeholder='Вибери або введи суму поповнення')
    reply_keyboard.row('30', '50', '120')
    reply_keyboard.add('Повернутися')
    send = bot.send_message(config.cid, 'Вибери суму оплати рахунку, або введи самомтійно', reply_markup=reply_keyboard)
    bot.register_next_step_handler(send, generate_payment_message)


def generate_payment_message(message):
    global payment_amount
    if message.text == 'Повернутися':
        command_start(message, 1)
    else:
        payment_amount = message.text

        inline_keyboard = types.InlineKeyboardMarkup()
        pay_url = get_url_from_payment_service(payment_method_variant, payment_amount)
        pay_text = 'Сплатити ' + payment_amount + ' грн'
        inline_keyboard.add(types.InlineKeyboardButton(pay_text, url=pay_url))
        bot.send_message(config.cid, 'Для здійснення оплати перейдіть за посиланням:', reply_markup=inline_keyboard)


def get_url_from_payment_service(service, amount):
    if service == 'Portmone':
        return 'https://www.portmone.com.ua/gateway/?PAYEE_ID=6813&CONTRACT_NUMBER=3658365&BILL_AMOUNT=' + amount
    elif service == 'iPay':
        return 'https://www.ipay.ua/ru/charger?bill_id=591&acc=3658365&invoice=' + amount
    elif service == 'PrivatBank':
        return 'https://my-payments.privatbank.ua/mypayments/customauth/identification/fp/static?staticToken=92b2d25e0c3c5e96f03cd5e386b30a43&acc=3658365&amount=' + amount


bot.polling()
