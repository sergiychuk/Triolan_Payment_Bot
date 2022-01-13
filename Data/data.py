# -*- coding: utf-8 -*-
import json
import datetime
import pytz

class BotData:
    # region ———[ Constructor ]———
    def __init__(self, account_id, payment_service):
        self._account_id = account_id  # accountid = 3658365
        self._payment_money_amount = 0  # money amount set  to 32 UAH by default
        self._payment_days_amount = 0  # days payment amount set by payment_money_amout
        self._payment_service = payment_service  # money amount set  to 32 UAH by default
        self._service_links = {
                'Portmone': f'https://www.portmone.com.ua/gateway/?PAYEE_ID=6813&CONTRACT_NUMBER={self.account_id}&BILL_AMOUNT={self.payment_money_amount}',
                'iPay': f'https://www.ipay.ua/ru/charger?bill_id=591&acc={self.account_id}&invoice={self.payment_money_amount}',
                }
    # endregion

    # region ———[ Properties ]———
    # region [Account ID]
    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value
    # endregion

    # region [Payment Money Amount]
    @property
    def payment_money_amount(self):
        return int(self._payment_money_amount)

    @payment_money_amount.setter
    def payment_money_amount(self, value):
        self._payment_money_amount = value
    # endregion

    # region [Payment Days Amount]
    @property
    def payment_days_amount(self):
        if self.payment_money_amount > 0:
            self._payment_days_amount = self.payment_money_amount / 4
        else:
            self._payment_days_amount = 0
        return int(self._payment_days_amount)

    @payment_days_amount.setter
    def payment_days_amount(self, value):
        self._payment_days_amount = value
        self.payment_money_amount = self._payment_days_amount * 4
    # endregion

    # region [Payment Service]
    @property
    def payment_service(self):
        return self._payment_service

    @payment_service.setter
    def payment_service(self, value):
        self._payment_service = value

    def get_payment_services_list(self):
        list = []
        for key in self._service_links.keys():
            list.append(key)
        return list

    # endregion

    # region [Payment Service]
    @property
    def services_links(self):
        return self._service_links

    @services_links.setter
    def services_links(self, value: dict):
        self._service_links = value
    # endregion

    # endregion

    # region ———[ Payment link with choosed service ]———
    def get_payment_link(self, service:str, money_amount=None, days_amount=None):
        if money_amount is not None:
            self.payment_money_amount = money_amount
        elif days_amount is not None:
            self.payment_money_amount = days_amount * 4

        if service in self._service_links:
            return self._service_links[service]
        else:
            return f'Service {service} not found!'
    # endregion
