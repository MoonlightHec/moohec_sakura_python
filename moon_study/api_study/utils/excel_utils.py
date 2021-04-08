# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/26 10:05 
# @Author : mhec 
# @File : excel_utils.py
# @desc :
"""
import xlrd


class get_excel_datas:
    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = xlrd.open_workbook(self.file_path)


