# _*_ coding: utf-8 _*_
"""
# @Time : 2021/2/20 17:01 
# @Author : River 
# @File : doubanPlus.py
# @desc :
"""
import collections
import os

import yaml

from moon_util import sort_yaml
from moon_spider.douban_spider.requestAttr import requestAttr
from moon_spider.douban_spider.spider_tool import get_soup, random_useragent, ip_filter, get_pools_threads


def get_playable(request_attr):
    """
    爬取播放源地址
    :param request_attr:
    :return:
    """
    source_list = [{}]

    soup = get_soup(request_attr)
    play_source = soup.find('ul', 'bs')
    if play_source:
        li_list = play_source.find_all('a')
        for each in li_list:
            source = each.text.strip()
            play_url = each.attrs['href']
            source_list[0][source] = play_url
    else:
        source_list[0]['在哪儿看这部电影'] = '找不到播放源'
    return source_list


def get_movies(request_attr):
    """
    组装所有的电影信息
    :param request_attr:
    :return:
    """
    movie_list = {}
    # 电影主要信息所在div
    soup = get_soup(request_attr)
    pic_list = soup.find_all('div', 'pic')
    for each in pic_list:
        movie = [{}]
        # 获取主要电影信息
        sort = each.find('em').text.strip()
        movie[0]['1-片名'] = each.img['alt']
        movie[0]['3-详情页'] = each.a['href']
        movie[0]['2-图片地址'] = each.img['src']
        # request_attr对象的url换成详情页面的url
        movie_attr = requestAttr(each.a['href'], request_attr.ip_list)
        movie[0]['4-播放源'] = get_playable(movie_attr)
        movie_list[int(sort)] = movie
        print("%s.《%s》获取成功！" % (sort, each.img['alt']))
    return movie_list


def main():
    if not os.path.exists('./pro_useful.yaml'):
        # 获取代理ip池
        get_pools_threads('云代理')
        # 校验可用ip
        url_filter = "https://movie.douban.com/top250?start="
        headers_filter = random_useragent()
        headers_filter.setdefault('Host', 'movie.douban.com')
        ip_filter(url_filter, headers_filter)

    # 获取ip代理集合
    with open('./pro_useful.yaml', 'r', encoding='utf8') as stream:
        pro_list = yaml.safe_load(stream)
    headers = {
        'Host': 'movie.douban.com'
    }
    path = './movies.yaml'
    if os.path.exists(path):
        os.remove(path)
    for offset in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start=' + str(offset)
        request_attr = requestAttr(url, pro_list, headers)
        # 得到当前页的所有movie信息
        movies = get_movies(request_attr)
        # 通过排序生成一个有序的字典OrderedDict
        sort_movies = collections.OrderedDict(sorted(movies.items(), key=lambda t: t[0], reverse=False))
        with open(path, 'a', encoding='utf8') as stream:
            sort_yaml.ordered_yaml_dump(sort_movies, stream, allow_unicode=True)


def get_ip():
    # 获取代理ip池
    # get_pools('云代理')
    get_pools_threads('云代理')

if __name__ == '__main__':
    main()
    # get_ip()
