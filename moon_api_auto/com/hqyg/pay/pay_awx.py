# _*_ coding: utf-8 _*_
"""
# @Time : 2021/9/9 11:25 
# @Author : lijun7 
# @File : pay_awx.py
# @desc :
"""
import uuid

import requests
from flask import json

from moon_util.cursor_util.DbTools import DbTools


class AWX_Test:
    def __init__(self):
        self.allDomains = {
            'apiDomain': 'https://api-demo.airwallex.com',
            'fileDomain': 'https://files-demo.airwallex.com',
            'paDomain': 'https://pci-api-demo.airwallex.com',
            'isDomain': 'https://pci-api-demo.airwallex.com'
        }
        self.client = {
            'clientId': '4OuJUnXeQuGF9jZuEhl8-Q',
            'apiKey': 'df2bc288be96410ef540d16290f00d67761d342af8f9774845d26c5428c72644e99e44ad86f89e32d7ad60b01a622ed1',
        }
        self.headers = {
            "Authorization": "Bearer {}".format(self.login()),
            "Content-Type": "application/json",
        }
        with open('./resource/awx_info.json', 'r', encoding='utf-8') as awx_st:
            self.awx_api_info = json.load(awx_st)

    def login(self):
        url = '{}/api/v1/authentication/login?api_key={}&client_id={}'.format(self.allDomains['paDomain'], self.client['apiKey'], self.client['clientId'])
        headers = {
            'Content-Type': 'application/json',
            'x-client-id': self.client['clientId'],
            'x-api-key': self.client['apiKey']
        }
        res = requests.post(url=url, headers=headers)
        token = res.json().get('token')
        # print("login token:\n{}".format(token))
        return token

    def create_payment(self, need_3ds=False):
        """
        create请求
        :param need_3ds:
        :return:
        """
        print('创建create请求：')
        url = '{}/api/v1/pa/payment_intents/create'.format(self.allDomains['paDomain'])
        headers = self.headers
        headers['x-api-version'] = "2021-02-28"
        body = self.awx_api_info.get('create')
        # 需要测试的参数
        body['request_id'] = str(uuid.uuid1())
        body['amount'] = 14314777.99
        body['currency'] = 'USD'
        body['merchant_order_id'] = str(uuid.uuid1())
        body['order']['shipping']['country_code'] = 'NL'
        body['order']['shipping']['street'] = 'addressLine1 addressLine2'
        body['return_url'] = 'http://www.example.com'
        # 是否3ds
        if need_3ds:
            body['payment_method_options']['card']['risk_params']['skip_risk_processing'] = 'true'
            body['payment_method_options']['card']['risk_params']['three_domain_secure_action'] = 'FORCE_3DS'
        res = requests.post(url, headers=headers, json=body)
        return res

    def confirm_payment(self, intent_id=''):
        """
        :param intent_id:
        :return:
        """
        print('创建confirm请求：')
        url = '{}/api/v1/pa/payment_intents/{}/confirm'.format(self.allDomains['paDomain'], intent_id)
        headers = self.headers
        body = self.awx_api_info.get('confirm')
        # 需要测试的参数
        body['request_id'] = str(uuid.uuid1())
        # 地址信息
        body['payment_method']['billing']['last_name'] = 'lijun'
        body['payment_method']['billing']['address']['country_code'] = 'GB'
        body['payment_method']['billing']['address']['street'] = 'addressLine1 addressLine2'
        body['payment_method']['billing']['address']['state'] = 'Stirling'
        body['payment_method']['billing']['address']['city'] = 'StirlingCity'
        # card信息
        body['payment_method']['card']['number'] = '4000000000001191'
        body['payment_method']['card']['expiry_month'] = '10'
        body['payment_method']['card']['expiry_year'] = '2031'
        body['payment_method']['card']['cvc'] = '121'
        body['payment_method']['card']['name'] = 'QIAO ZHAO'

        res = requests.post(url, headers=headers, json=body)
        return res

    def refunds(self, amount, transaction_id):
        url = '{}/api/v1/pa/refunds/create'.format(self.allDomains['paDomain'])
        headers = self.headers
        body = {
            "payment_intent_id": transaction_id,
            "reason": "Return good",
            "amount": amount,
            "request_id": str(uuid.uuid1())
        }
        res = requests.post(url, headers=headers, json=body)
        return res

    def get_payment(self, transaction_id):
        url = '{}/api/v1/pa/payment_intents/{}'.format(self.allDomains['paDomain'], transaction_id)
        headers = self.headers
        res = requests.get(url, headers=headers)
        self.preview(res)

    def get_refunds(self, payment_intent_id):
        """
        查询awx退款记录
        :param payment_intent_id:
        :return:
        """
        url = '{}/api/v1/pa/refunds'.format(self.allDomains['paDomain'])
        params = {
            "payment_intent_id": payment_intent_id
        }
        res = requests.get(url, headers=self.headers, params=params)
        if res.status_code == 200:
            self.preview(res)

    def preview(self, response):
        print(json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))

    def run_create(self):
        # 创建create
        res_create = self.create_payment()
        # preview(res_create)
        if res_create.status_code == 201:
            creat_card_info = res_create.json()['available_payment_method_types']
            print('available_payment_method_types:\n%s' % creat_card_info)
            if 'card' in creat_card_info:
                payment_intent_id = res_create.json()['id']
                print(payment_intent_id)
        return payment_intent_id

    def run_confirm(self):
        # 创建confirm
        res_confirm = self.confirm_payment(intent_id=self.run_create())
        if res_confirm.status_code == 200:
            confirm_status = res_confirm.json()['status']
            url = res_confirm.json()['next_action']['url']
            jwt = res_confirm.json()['next_action']['data']['jwt']
            print('confirm_status:【%s】' % confirm_status)
            print('url:{}\njwt:{}'.format(url, jwt))

    def run_refunds(self, amount, pay_sn):
        db = DbTools('PAY')
        sql = "SELECT transaction_id FROM pay_gateway_31  WHERE pay_sn = '%s';"
        cursor = db.cursor
        cursor.execute(sql % pay_sn)
        if cursor.rowcount:
            transaction_id = cursor.fetchone()[0]
        del db
        print('transaction_id:'.format(transaction_id))
        res_refunds = self.refunds(amount, transaction_id)
        self.preview(res_refunds)


if __name__ == '__main__':
    intent_id = 'int_hkdmwnlxhg2ldekh4b3'
    awx_pay_sn = 'U2108163227423001'
    awx_cc = AWX_Test()
    # awx_cc.run_refunds(amount=10, pay_sn=awx_pay_sn)
    awx_cc.get_payment(intent_id)
    # awx_cc.get_refunds(intent_id)
