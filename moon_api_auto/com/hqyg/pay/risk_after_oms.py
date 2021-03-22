# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/15 10:01 
# @Author : River 
# @File : risk_after_oms.py
# @desc : oms推送事后风控结果
"""
from moon_api_auto.pytest_util.HttpUtils import HttpRequest


def get_after_risk():
    """
    oms推送事后风控信息到支付
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}
    pay_sn = 'P210315013287190346GMN'
    data = {
        "header": {
            "service": "com.globalegrow.risk.api.core.RiskCoreService",

            "method": "afterRiskProcessor",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": {
            "paySn": pay_sn, "omsId": ""
        }
    }
    response = HttpRequest.post(url=url, headers=headers, body=data)
    print(response.get('preview'))


if __name__ == '__main__':
    get_after_risk()
