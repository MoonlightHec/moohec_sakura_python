# _*_ coding: utf-8 _*_
"""
# @Time : 2021/7/13 17:33 
# @Author : lijun7 
# @File : zaful_create_order.py
# @desc :
"""
import hashlib
import sys

import requests

from moon_api_auto.com.hqyg.oms.WebminObj import WebminObj
from moon_api_auto.pytest_util.http_utils import HttpRequest
from moon_util.cursor_util.DbTools import DbTools

# 禁用安全警告信息；requests忽略ssl证书后，控制台不再输出警告信息
requests.packages.urllib3.disable_warnings()


def push_mq(order_sn, joint=False):
    """
    2.前端网站推送订单到MQ
    :param order_sn: 订单号
    :param joint: 是否是联合订单
    :return:
    """
    if joint:
        # 联合订单
        url = 'http://www.pc-zaful-master-php5.fpm.egomsl.com/eload_admin/crontab/xcmq/warehouse/OrderToOmsApi.php?order_sn=%s' % order_sn
    else:
        # 普通订单
        url = 'http://www.pc-zaful-master-php5.fpm.egomsl.com/eload_admin/crontab/xcmq/order_to_oms_api.php?order_sn=%s' % order_sn
    response = HttpRequest.get(url)
    print(response)


def audit_payment(order_sn):
    """
    4.审核付款单
    :param order_sn:订单号
    :return:
    """

    db_tools = DbTools('OMS')
    connect = db_tools.connect
    cursor = db_tools.cursor
    sql = "UPDATE f_oms_payment_info SET matched_status=1 WHERE order_sn=\'%s\';"
    cursor.execute(sql % order_sn)
    connect.commit()
    del db_tools


def match_order(match_name=None, order_sn=None):
    """
    5.匹配订单
    :param order_sn: 订单编号
    :param match_name: 匹配脚本名称
    match_payment_info_cb：匹配正常CB订单
    match_payment_info：匹配除CB外的正常订单
    match_payment_info_nopay：匹配服装、电子的COD订单
    match_payment_info_cb_nopay：匹配CB的COD订单
    :return:
    """
    web_script = WebminObj(match_name)
    web_script.run_script(args=order_sn)


def md5(string):
    m = hashlib.md5()
    m.update(string.encode("utf8"))
    print("加密前：【{}】,加密后：【{}】".format(string, m.hexdigest()))
    return m.hexdigest()


def joint_order_2oms(order_sn, step=0):
    if step == 0:
        # 网站推送订单
        push_mq(order_sn, joint=True)
    elif step == 1:
        # oms导入脚本
        web_soaOrder_received = WebminObj('soa_mq_oms_received')
        web_soaOrder_received.run_script()
    elif step == 2:
        # 投递脚本
        web_soaOrder_intoMq = WebminObj('soa_order_into_mq')
        web_soaOrder_intoMq.run_script(order_sn, md5(order_sn)[:2])
    elif step == 3:
        # 消费脚本
        web_soaOrder_into_oms = WebminObj('get_soa_mq_into_oms')
        web_soaOrder_into_oms.run_script()
    else:
        return


if __name__ == '__main__':
    oms_order_sn = 'U2108310352544644S001'
    # 网站MQ推送订单到oms
    # push_mq(oms_order_sn, joint=True)
    # 审核付款单
    # audit_payment(oms_order_sn)
    # 匹配订单
    # match_order(match_name='match_payment_info_nopay', order_sn=oms_order_sn)
    # 联合订单推送到oms
    joint_order_2oms(oms_order_sn, step=2)
