# -*- coding: utf-8 -*-
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import copy
from keyboa import Keyboa, Button

import Config
from Data import data

class KeyboardClass:

    # region ---[Constructor]---
    def __init__(self) -> None:
        self.btn_cancel = Button(button_data=('❌ ⲟⲧⲙⲉⲏⲁ', 'cancel'), front_marker='cb_').button
        self.btn_back = Button(button_data=('◀️ ⲏⲁⳅⲁⲇ', 'back'), front_marker='cb_').button

        self.btn_contract_id = Button(button_data=('🆔 ⲏⲟⲙⲉⲣ ⲇⲟⲅⲟⲃⲟⲣⲩ', 'contract_id'), front_marker='change ').button
        self.btn_payment_system = Button(button_data=('💰 плᴀтіжнᴀ систᴇмᴀ', 'payment_system'), front_marker='change ').button
        self.btn_days_amount = Button(button_data=('📆 ⲕіⲗьⲕіⲧь ⲇⲏіⲃ', 'days_amount'), front_marker='change ').button
        self.btn_money_amount = Button(button_data=('💵 ⲥⲩⲙⲁ ⲡⲗⲁⲧⲉⲿⲩ', 'money_amount'), front_marker='change ').button
    # endregion

    # region ---[Keyboards]---
    # region Main menu
    @property
    def main_menu(self):
        # BUTTONS
        btn_gen_payment_link = Button(button_data=('💸 ⲥⲡⲗⲁⲧυⲧυ', 'payment_link'), front_marker='show ').button
        menu_buttons = [self.btn_contract_id,
                        self.btn_payment_system,
                        self.btn_days_amount,
                        self.btn_money_amount,
                        btn_gen_payment_link]
        # ADD BUTTONS TO KEYBOARD
        keyboard = Keyboa(items=menu_buttons, items_in_row=1).keyboard
        return keyboard
    # endregion

    # region Days amount change
    @property
    def days_amount_menu(self):
        btn_back = copy.deepcopy(self.btn_back)
        btn_back.callback_data = 'return main_menu'

        self.btn_days_amount_increase = Button(button_data=('🔼', 'increase'), front_marker='days_amount ').button
        self.btn_days_amount_decrease = Button(button_data=('🔽', 'decrease'), front_marker='days_amount ').button

        value_controll = [[self.btn_days_amount_increase, self.btn_days_amount_decrease], ]
        days = list(range(4, 28, 4))
        controlls = [[btn_back], ]

        keyboard_value_controll = Keyboa(items=value_controll).keyboard
        keyboard_days = Keyboa(items=days, items_in_row=6, front_marker='set_days_amount ').keyboard
        keyboard_controlls = Keyboa(items=controlls).keyboard

        keyboard = Keyboa.combine(keyboards=(keyboard_value_controll, keyboard_days))
        keyboard = Keyboa.combine(keyboards=(keyboard, keyboard_controlls))
        return keyboard
    # endregion

    # region Money amount change
    @property
    def money_amount_menu(self):
        btn_back = copy.deepcopy(self.btn_back)
        btn_back.callback_data = 'return main_menu'

        btn_money_amount_increase = Button(button_data=('➕➕➕', 'increase'), front_marker='money_amount ').button
        btn_money_amount_decrease = Button(button_data=('➖➖➖', 'decrease'), front_marker='money_amount ').button

        value_controll = [[btn_money_amount_increase, btn_money_amount_decrease], ]
        money_values = list(range(4, 132, 8))
        controlls = [[btn_back], ]

        keyboard_value_controlls = Keyboa(items=value_controll).keyboard
        keyboard_money = Keyboa(items=money_values, items_in_row=4, front_marker='set_money_amount ').keyboard
        keyboard_controlls = Keyboa(items=controlls).keyboard

        keyboard = Keyboa.combine(keyboards=(keyboard_value_controlls, keyboard_money))
        keyboard = Keyboa.combine(keyboards=(keyboard, keyboard_controlls))
        return keyboard
    # endregion

    # region Payment system change
    @property
    def payment_system_menu(self):
        btn_back = copy.deepcopy(self.btn_back)
        btn_back.callback_data = 'return main_menu'
        payment_systems = data.get_payment_services_list()
        controlls = [[btn_back], ]
        keyboard_payment_systems = Keyboa(items=payment_systems,
                                          items_in_row=4,
                                          front_marker='set_payment_system ').keyboard
        keyboard_controlls = Keyboa(items=controlls).keyboard
        keyboard = Keyboa.combine(keyboards=(keyboard_payment_systems, keyboard_controlls))
        return keyboard
    # endregion

    # region Contract ID
    @property
    def contract_id_menu(self):
        btn_back = copy.deepcopy(self.btn_back)
        btn_back.callback_data = 'return main_menu'

        controlls = [[btn_back], ]

        keyboard = Keyboa(items=controlls).keyboard
        return keyboard
    # endregion

    # region Payment Link
    @property
    def payment_link_menu(self):
        markup = InlineKeyboardMarkup()
        btn_do_payment = InlineKeyboardButton(text='СПЛАТИТИ',
                                              url="https://www.portmone.com.ua/gateway/?PAYEE_ID=6813&CONTRACT_NUMBER=3658365&BILL_AMOUNT=32",
                                              callback_data="cb_yes")
        markup.add(btn_do_payment)
        return markup

        # btn_back = copy.deepcopy(self.btn_back)
        # btn_back.callback_data = 'return main_menu'
        # btn_open_payment_link = Button(button_data=('ⲥⲡⲗⲁⲧυⲧυ', 'payment_link'), front_marker='show ').button
        #
        # controlls = [[btn_back], ]
        #
        # keyboard = Keyboa(items=controlls).keyboard
        # return keyboard
    # endregion

    # endregion [Keyboards]
