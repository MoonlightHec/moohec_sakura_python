# _*_ coding: utf-8 _*_
"""
# @Time : 2021/4/9 14:58 
# @Author : mhec 
# @File : area_tag_test.py
# @desc :
"""

from moon_api_auto.pytest_util.http_utils import HttpRequest


def area_country_list():
    url = 'http://www.obs-pay.com/pay/channel-country/area-country-list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Cookie': 'S_SESSIONID=jhpv8a09a1phddq5k5u9d0nchh;SITECODE=ZF'
    }
    params = {
        'pageNo': '1',
        'pageSize': '1000'
    }
    response = HttpRequest.get(url=url, headers=headers, params=params)
    print(response.get('preview'))


if __name__ == '__main__':
    area_country_list()
