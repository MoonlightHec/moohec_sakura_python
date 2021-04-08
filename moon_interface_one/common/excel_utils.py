# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/26 9:59 
# @Author : mhec 
# @File : excel_utils.py
# @desc :
"""
import traceback

import xlrd


class ExcelDatas:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.workbook, self.sheet, self.mode = self.get_wb(file_path, sheet_name)
        if self.mode == 1:
            self.rowNum = self.sheet.nrows
            self.colNum = self.sheet.ncols

    @staticmethod
    def get_wb(file_path, sheet_name):
        wb = None
        sheet = None
        try:
            wb = xlrd.open_workbook(file_path)
            sheet = wb.sheet_by_name(sheet_name)
            mode = 1
        except FileNotFoundError:
            # traceback.print_exc()
            mode = 2
            print('文件路径不存在')
        except xlrd.biffh.XLRDError:
            # traceback.print_exc()
            print('sheet名称不正确')
            mode = 3
        return wb, sheet, mode

    def read_data(self, row_num, col_num):
        """读取指定单元格的数据"""
        if self.mode == 1:
            return self.sheet.cell(row_num, col_num).value

    def __read_datas(self, start_row=None, end_row=None, start_col=None, end_col=None):
        """
        获取excel指定范围数据
        :param start_row: 开始行号（不包含，第一行号为1）
        :param end_row: 结束行号（包含）
        :param start_col: 开始列号（不包含，第一列号为0）
        :param end_col: 结束列号（包含）
        :return:
        """
        if self.mode == 1:
            # 读取所有数据
            if start_row is None and end_row is None and start_col is None and end_col is None:
                return self.__real_read_datas(1, self.rowNum, 1, self.colNum)
            # 读取指定行，列数据
            elif start_row is not None and end_row is not None and start_col is not None and end_col is not None:
                return self.__real_read_datas(start_row, end_row, start_col, end_col)
            else:
                print(u"想要获取的数据范围不正确")

    def run_case_number(self, number_list=None):
        """指定跑哪条用例"""
        if self.mode == 1:
            case_datas = []
            if number_list:
                for num in number_list:
                    row_data = self.__read_datas(start_row=num, end_row=num + 1, start_col=0, end_col=self.colNum)
                    case_datas.append(row_data[0])
            else:
                print(u"要执行的用例编号不存在")
            return case_datas

    def __real_read_datas(self, start_row=None, end_row=None, start_col=None, end_col=None):
        """实际读取excel文件方法"""
        datas = []
        try:
            for i in range(start_row, end_row):
                sheet_data = []
                for j in range(start_col, end_col):
                    c_cell = self.sheet.cell_value(i, j)
                    if j == 0:
                        c_cell = int(c_cell)
                    sheet_data.append(c_cell)
                datas.append(sheet_data)
        except IndexError:
            # traceback.print_exc()
            print(u"想要获取的数据范围不正确")
        return datas
