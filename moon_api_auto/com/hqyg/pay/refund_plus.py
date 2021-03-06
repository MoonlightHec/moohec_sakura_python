# _*_ coding: utf-8 _*_
"""
# @Time : 2021/4/28 16:22 
# @Author : mhec 
# @File : refund_plus.py
# @desc : 停止checkout服装旧收款账号的API自动退款请求
"""
import os
import random

from flask import json

from moon_api_auto.pytest_util.http_utils import HttpRequest
from moon_util import sort_yaml
from moon_util.cursor_util import db

path = './resource/refund_cases'
refund_account = ['uzaW2LIr9s7IaKo+406V4DYQopUVKibn15vd0HwKOerH+Vv7qg1NIgnuW6sDfFi6Fsvr05mXQ7jBjbjtg7lNuw==',
                  'oL55iTIWXR+RSkd25Y7nHbOVvD9iAOGu8Z9DunZaTD1pfJNkGEFzIQJFTi4AZkBJyPmHqZlopMQRqI4mKAXHEQ==']


def refund(method=1, refund_type=0):
    """
    退款接口
    :param refund_type: 0原路退 1退电子钱包
    :param method: 1退款 2提现
    :return:
    """

    case_data = sort_yaml.ordered_yaml_load(path)
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}
    data = {
        "header": {
            "service": "com.globalegrow.spi.pay.inter.RefundService",
            "method": "refund",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": {
            "orderSn": case_data['order_sn'],
            "refundAccountId": 2359975,
            "refundDtos": [{
                "amount": case_data['amount'],
                "channelCode": case_data['channel'],
                "currencyAmount": case_data['currency_amount'],
                "currencyCode": case_data['currency_code'],
                "currencyRate": case_data['currency_rate'],
                "omsTxId": case_data['pay_sn'],
                "paySn": case_data['pay_sn']
            }],
            "refundType": refund_type,  # 0原路退 1电子钱包
            "remark": "一级原因:客户原因退款,二级原因:忘记使用折扣码",
            "siteCode": case_data['siteCode'],
            "sourceId": 'TKSQ2018070422' + str(random.randint(100000, 999999)),
            "userEmail": "lijun7@globalegrow.com",
            "userId": case_data['user_id']
        }
    }
    data_withdrawal = {
        "header": {
            "service": "com.globalegrow.spi.pay.inter.RefundService",
            "method": "withdrawal",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": {
            "userId": case_data['user_id'],
            "siteCode": case_data['siteCode'],
            "withdrawalInfoList": [
                {
                    "paySn": case_data['pay_sn'],
                    "channelCode": case_data['channel'],
                    "withdrawalAmount": case_data['amount'],
                    "sourceId": 'TKSQ2018070422' + str(random.randint(100000, 999999)),
                    "withdrawalAccountId": str(random.randint(100000000000, 999999999999)),
                    "withdrawalCurrencyAmount": case_data['currency_amount'],
                    "withdrawalCurrencyCode": case_data['currency_code'],
                    "withdrawalCurrencyRate": case_data['currency_rate']
                }
            ]
        }
    }
    if method == 2:
        data = data_withdrawal
    refund_output = HttpRequest.post(url=url, headers=headers, body=data)
    refund_params = json.dumps(data, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
    return refund_params, refund_output


def get_case_datas(pay_gateway_id=31, pay_id=None, pay_sn=None):
    """
    获取订单信息
    :param pay_sn:
    :param pay_gateway_id: 订单所在gateway分表序号
    :param pay_id: 数据主键id
    :return:
    """
    where = 'id'
    value = pay_id
    if pay_sn:
        where = 'pay_sn'
        value = pay_sn
    sql = 'SELECT id,parent_order_sn,pay_status,pay_sn,pay_account,site_code,currency_code,pay_amount,channel_code,' \
          'currency_code,currency_rate,pay_currency_amount,user_id FROM pay_gateway_%s WHERE %s ="%s";' % (pay_gateway_id, where, value)
    connect = db.get_connect('PAY')
    cursor = connect.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        case_data = {
            'des': row[5],
            'order_sn': row[1],
            'pay_sn': row[3],
            'siteCode': row[5],
            'amount': float(row[7]),
            'account': row[4],
            'currency_amount': float(row[11]),
            'message': None,
            'success': None,
            'currency_code': row[9],
            'currency_rate': float(row[10]),
            'channel': row[8],
            'user_id': row[12]
        }
    if os.path.exists(path):
        os.remove(path)
    for i in range(0, cursor.rowcount):
        with open(path, 'a', encoding='utf8') as stream:
            sort_yaml.ordered_yaml_dump(case_data, stream, allow_unicode=True)


get_case_datas(pay_sn='P210519013287182139BXM')
params, output = refund()
print(u'请求参数：\n%s' % params)
print(u'返回参数：\n%s' % output.get('preview'))
