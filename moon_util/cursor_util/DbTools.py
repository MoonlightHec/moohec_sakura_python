# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/27 9:10 
# @Author : lijun7 
# @File : DbTools.py
# @desc :
"""
import os

import pymysql

from moon_util import sort_yaml


class DbTools:
    def __init__(self, name):
        path = r'/db_hqyg_config.yaml'
        # 获取当前文件db.py绝对路径
        db_path = os.path.dirname(os.path.abspath(__file__))
        datas = sort_yaml.ordered_yaml_load(db_path + path)

        db_config = datas[name]
        self.connect = pymysql.connect(**db_config)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    db = DbTools('OMS')
    print()
