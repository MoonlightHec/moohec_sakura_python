# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/16 14:56 
# @Author : River 
# @File : refund.py
# @desc : 退款接口
"""
import random

from moon_api_auto.pytest_util.http_utils import HttpRequest


def refund():
    """
    付款单退款，注意事项：站点、汇率、退款金额
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    source_id = 'TKSQ2018070422' + str(random.randint(100000, 999999))
    order_sn = 'ZP1808080757490237'
    pay_sn = 'P180808007864205849104'
    siteCode = 'RG'
    currencyRate = 1.0000000000
    amount = 45.84
    data = {
        "header": {
            "service": "com.globalegrow.spi.pay.inter.RefundService",
            "method": "refund",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": {
            "orderSn": order_sn,
            "refundAccountId": 2359975,
            "refundDtos": [{
                "amount": amount,
                "channelCode": "checkout_credit",
                "currencyAmount": amount,
                "currencyCode": "USD",
                "currencyRate": currencyRate,
                "omsTxId": pay_sn,
                "paySn": pay_sn
            }],
            "refundType": 0,
            "remark": "一级原因:客户原因退款,二级原因:忘记使用折扣码",
            "siteCode": siteCode,
            "sourceId": source_id,
            "userEmail": "lijun7@globalegrow.com",
            "userId": 188265
        }
    }
    response = HttpRequest.post(url=url, headers=headers, body=data)
    print(response.get('preview'))


if __name__ == '__main__':
    refund()
