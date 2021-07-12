# _*_ coding: utf-8 _*_
"""
# @Time : 2021/6/16 16:46 
# @Author : lijun7 
# @File : cookies_test.py
# @desc :
"""
import os
import pickle

from selenium import webdriver

request_url = "https://www.forever21.com/us/shop/catalog/category/f21/women-new-arrivals-clothing-dresses"


def get_cookies():
    driver = webdriver.Chrome()
    driver.get(request_url)
    data = driver.get_cookies()
    driver.quit()
    cookies = {}
    for item in data:
        cookies[item['name']] = item['value']
    with open('./forever.pickle', 'wb') as output:
        pickle.dump(cookies, output)
    return cookies


def read_cookies():
    if os.path.exists('forever.pickle'):
        readPath = open('forever.pickle', 'rb')
        forever_cookies = pickle.load(readPath)
    else:
        forever_cookies = get_cookies()
    return forever_cookies


if __name__ == '__main__':
    print(read_cookies())
