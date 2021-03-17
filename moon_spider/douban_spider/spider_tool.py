# _*_ coding: utf-8 _*_
"""
# @Time : 2021/2/24 14:39 
# @Author : River 
# @File : ip_useful.py
# @desc :
"""
import os
import random
import threading
import time

import requests
import yaml
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import TooManyRedirects

from moon_spider.douban_spider.requestAttr import requestAttr
from moon_util import sort_yaml

ip_pool_path = './ip_pools.yaml'  # ip池


def random_useragent():
    """
    获取一个随机User-Agent的headers
    :return:
    """
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    return headers


def ip_filter(url, headers):
    """
    测试代理ip是否可用
    :return:
    """
    ip_useful_path = './pro_useful.yaml'  # 可用ip
    pro_list = sort_yaml.ordered_yaml_load(ip_pool_path)
    # 可用ip储存位置
    if os.path.exists(ip_useful_path):
        os.remove(ip_useful_path)
    key = 0
    for pro in pro_list:
        try:
            pro_info = {}
            time.sleep(1)
            requests.get(url=url, headers=headers, proxies={'http': pro_list[pro]})
            print('ip_filter校验ip可用：%s' % pro_list[pro])
            key += 1
            pro_info[key] = pro_list[pro]
            with open(ip_useful_path, 'a', encoding='utf8') as stream:
                sort_yaml.ordered_yaml_dump(pro_info, stream, allow_unicode=True)
        except TooManyRedirects:
            print('ip_filter校验ip不可用:%s' % pro_list[pro])


def get_soup(request_attr):
    """
    获取整个页面soup对象
    :param request_attr:
    :return:
    """
    # 使用指定代理ip
    if request_attr.ip:
        requests_ip = request_attr.ip
    # 获取一个随机代理ip
    elif request_attr.ip_list:
        key = random.sample(request_attr.ip_list.keys(), 1)
        requests_ip = request_attr.ip_list[key[0]]
    # 不使用代理ip
    else:
        requests_ip = None
    # 获取一个随机User-Agent
    headers = random_useragent()
    if request_attr.headers:
        headers = {**headers, **request_attr.headers}
    time.sleep(random.randint(0, 2) + random.random())
    try:
        print("请求ip：%s" % requests_ip)
        r = requests.get(url=request_attr.url, headers=headers, proxies={'http': requests_ip})
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
    except TooManyRedirects:
        print("此ip不可用：%s" % requests_ip)
        get_soup(request_attr)
    return soup


def write_ip(index_ip, index_ip_range):
    for i in range(index_ip_range[0], index_ip_range[1]):
        ip_info_dict = {}
        key = 10 * i
        request_attr = requestAttr(url=index_ip[i])
        soup = get_soup(request_attr)
        tbody = soup.find('tbody')
        tr_list = tbody.find_all('tr')
        for each in tr_list:
            key += 1
            td = each.find_all('td')
            ip = td[0].text.strip() + ':' + td[1].text.strip()
            ip_info_dict[key] = ip
        print(ip_info_dict)
        with open(ip_pool_path, 'a', encoding='utf-8') as a:
            yaml.safe_dump(ip_info_dict, a, allow_unicode=True)


def get_pools_threads(url_name):
    """
    多线程获取ip池
    :param url_name:网站名称
    :return:
    """
    # ip_pool_path = './ip_pools.yaml'
    # 读取网站配置
    ip_url_path = 'resource/ip_url.yaml'
    with open(ip_url_path, 'r', encoding='utf-8') as r:
        ip_info = yaml.safe_load(r)
    url1 = ip_info[url_name][0]['url_p1']
    url2 = ip_info[url_name][0]['url_p2']
    page_list = ip_info[url_name][0]['page_list']

    # 删除历史文件
    if os.path.exists(ip_pool_path):
        os.remove(ip_pool_path)

    # 生成ip池文件
    index_ip = []
    for index in range(page_list[0], page_list[1], page_list[2]):
        url = url1 + str(index) + url2
        index_ip.append(url)
    index_ip_range = [(0, 4), (5, 10)]
    threads = []
    for i in range(0, 2):
        t = threading.Thread(target=write_ip, args=(index_ip, index_ip_range[i]))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
