# _*_ coding: utf-8 _*_
"""
# @Time : 2021/7/13 17:33 
# @Author : lijun7 
# @File : zaful_create_order.py
# @desc :
"""
import requests
from flask import json

from moon_api_auto.pytest_util.http_utils import HttpRequest

# 禁用安全警告信息；requests忽略ssl证书后，控制台不再输出警告信息
from moon_util.cursor_util import db

requests.packages.urllib3.disable_warnings()


def push_mq(order_sn):
    """
    2.推送MQ
    """
    url = 'http://www.pc-zaful-master-php5.fpm.egomsl.com/eload_admin/crontab/xcmq/order_to_oms_api.php?order_sn=%s' % order_sn
    response = HttpRequest.get(url)
    print(response)


def audit_payment(order_sn):
    """
    4.审核付款单
    :param order_sn:
    :return:
    """
    connect = db.get_connect('OMS')
    cursor = connect.cursor()
    sql = "UPDATE f_oms_payment_info SET matched_status=1 WHERE order_sn=\'%s\';"
    cursor.execute(sql % order_sn)
    connect.commit()
    cursor.close()
    connect.close()


def match_order(order_sn='21042300987314514995'):
    """
    5.匹配订单
    :return:
    """
    url = 'https://10.60.34.197:8100/session_login.cgi'
    headers = {
        "Cookie": "testing=1; sid=x"
    }
    data = {
        "page": "/",
        "user": "oms",
        "pass": "aTb8R3Rm2G9",
        "save": 1
    }
    # 获取cookies
    res = requests.post(url=url, headers=headers, data=data, verify=False, allow_redirects=False)
    cookiejar = res.cookies
    cookie = requests.utils.dict_from_cookiejar(cookiejar)
    headers['Cookie'] = 'testing=1; sid={}'.format(cookie['sid'])
    headers['Referer'] = 'https://10.60.34.197:8100/cron/edit_cron.cgi?idx=504'

    # 开始执行脚本
    save_url = 'https://10.60.34.197:8100/cron/save_cron.cgi'
    with open('./resource/webmin_match_order', 'r', encoding='utf8') as stream:
        data = json.load(stream)
        data['cmd'] = "php /data/www/devel/oms/daemon/payment/auto_match_payment_info.php  45  --order_sn {}".format(order_sn)
    # 保存脚本
    # 禁止重定向，否则重定向到/cron/exec_cron.cgi后，执行会因为没有cookie导致执行脚本报权限不足
    save_res = requests.get(url=save_url, headers=headers, params=data, verify=False, allow_redirects=False)
    print(save_res.text)
    # 执行脚本
    exec_res = requests.get(url='https://10.60.34.197:8100/cron/exec_cron.cgi?idx=504', headers=headers, verify=False)
    print(exec_res.text)


if __name__ == '__main__':
    oms_order_sn = 'U2108152109413287'
    # MQ推送订单到oms
    # push_mq(oms_order_sn)
    # 审核付款单
    # audit_payment(oms_order_sn)
    # 匹配订单
    match_order(oms_order_sn)
