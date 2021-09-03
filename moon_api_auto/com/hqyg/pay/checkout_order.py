# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/17 14:49 
# @Author : lijun7 
# @File : checkout_order.py
# @desc : 生成收银台页面
"""
import time

import requests
from flask import json


def checkout_order(country_name='美国'):
    """
    网站造单，生成收银台页面
    :param country_name: 收货国家简码
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    with open('./resource/checkout_order.json', 'r', encoding='utf8') as order_stream:
        body = json.load(order_stream)

    # 自动生成订单号
    order_sn = 'U2108{}{}'.format(int(time.time()), '01')

    # 获取收货国家信息
    with open('./resource/address_book.json', 'r', encoding='utf-8') as fd:
        address = json.load(fd)

    body['orderInfos'][0]['orderSn'] = order_sn
    body['orderInfos'][0]['orderAddressInfo']['firstName'] = address[country_name]['firstName']
    body['orderInfos'][0]['orderAddressInfo']['lastName'] = address[country_name]['lastName']
    body['orderInfos'][0]['orderAddressInfo']['countryCode'] = address[country_name]['countryCode']
    body['orderInfos'][0]['orderAddressInfo']['countryName'] = address[country_name]['countryName']
    body['orderInfos'][0]['orderAddressInfo']['state'] = address[country_name]['state']
    body['orderInfos'][0]['createTime'] = int(time.time())
    body['parentOrderSn'] = order_sn
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
    checkout_order("美国")
