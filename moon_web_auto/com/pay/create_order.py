# _*_ coding: utf-8 _*_
"""
# @Time : 2021/7/16 17:08 
# @Author : lijun7 
# @File : create_order.py
# @desc :
"""
from moon_web_auto.mysuites.webkeys import WebKey


class create_order:
    """
    造单
    """

    def __init__(self):
        self.web = WebKey()

    def setup_class(self):
        """
        构造函数，创建对象的时候会执行
        :return:
        """
        self.web.open_browser()

    def teardown_class(self):
        self.web.quit()

    def zf_order(self):
        self.web.geturl('http://user.pc-zaful-master-php5.fpm.egomsl.com/m-users-a-order_list.htm')
        self.web.input('','lijun7@globalegrow.com')
