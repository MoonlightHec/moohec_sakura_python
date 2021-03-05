# _*_ coding: utf-8 _*_
"""
# @Time : 2021/1/8 16:03 
# @Author : River 
# @File : params.py
# @desc :
"""
from moon_util.sort_yaml import ordered_yaml_load

datas = None
# 读取数据驱动的参数

datas = ordered_yaml_load('./ddt/login_page.yaml')

# 读取的yaml文件是乱序的，导致用例执行失败
# with open('../ddt/login_page.yaml', encoding='utf8') as f:
#     datas = yaml.safe_load(f)
