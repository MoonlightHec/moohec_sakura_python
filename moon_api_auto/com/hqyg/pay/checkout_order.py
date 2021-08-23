# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/17 14:49 
# @Author : lijun7 
# @File : checkout_order.py
# @desc :
"""
import time

import requests
from flask import json


def checkout_order(order_sn=None):
    """
    网站checkout生成收银台
    :param order_sn:
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    with open('./resource/checkout_order.json', 'r', encoding='utf8') as order_stream:
        body = json.load(order_stream)
    if not order_sn:
        order_sn = 'U2108{}{}'.format(int(time.time()), '01')
    body['orderInfos'][0]['orderSn'] = order_sn
    body['orderInfos'][0]['orderAddressInfo']['countryCode'] = 'NL'
    body['parentOrderSn'] = order_sn
    body['userInfo']['createTime'] = int(time.time())
    data = {
        "header": {
            "service": "com.globalegrow.spi.pay.inter.PayService",
            "method": "checkout",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": body
    }
    response = requests.post(url=url, headers=headers, json=data)
    res_body = response.json()['body']
    if res_body:
        json_body = json.loads(res_body)
        print('order_sn:%s' % order_sn)
        print('token:%s' % json_body['data']['token'])
        print('收银台链接:%s' % json_body['data']['redirectUrl'])
    else:

        print(json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


if __name__ == '__main__':
    checkout_order()
