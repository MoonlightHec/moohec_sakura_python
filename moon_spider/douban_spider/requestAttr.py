# _*_ coding: utf-8 _*_
"""
# @Time : 2021/2/24 17:08 
# @Author : River 
# @File : requestAttr.py
# @desc :
"""


class requestAttr:

    def __init__(self, url, ip_list={}, headers=None, ip=None):
        self.url = url
        self.ip_list = ip_list
        self.headers = headers
        self.ip = ip
