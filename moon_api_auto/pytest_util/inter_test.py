# _*_ coding: utf-8 _*_
"""
# @Time : 2021/2/5 14:44 
# @Author : River 
# @File : inter_test.py
# @desc :
"""
from moon_api_auto.pytest_util.http_utils import HttpRequest


def headers_test():
    url = 'http://127.0.0.1:5000/test_2.0'
    headers = {"Content-Type": "application/json"}
    params = {"name": "jyx", "age": "24"}
    preview = HttpRequest.post(url, headers, params)
    print(preview)


def get_http():
    url = 'http://127.0.0.1:5000/test_1.0?name=哈哈&age=18'
    preview = HttpRequest.get(url)
    print(preview)


def post_http():
    url = 'http://127.0.0.1:5000/test_2.0'
    headers = {"Content-Type": "application/json"}
    data = {'name': 'jy', 'age': '29'}
    preview = HttpRequest.post(url=url, headers=headers, body=data)
    print(preview)



