# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/26 16:36 
# @Author : mhec 
# @File : test_temp.py
# @desc : 获取excel数据例子
"""

import pytest
from flask import json

from moon_api_auto.pytest_util.http_utils import HttpRequest
from moon_interface_one.common.excel_utils import ExcelDatas


def get_datas():
    file_path = r'E:\Python\PycharmProjects\moohec_sakura_python\moon_interface_one\data\角色管理.xlsx'
    excelDatas = ExcelDatas(file_path=file_path, sheet_name='requestUrl')
    datas = excelDatas.run_case_number([1, 2, 3])
    return datas


class TestAddRole:
    case_data = get_datas()

    @pytest.mark.parametrize('role_data', case_data)
    def test_add_role(self, role_data):
        headers = {
            "Content-Type": "application/json",
            "PLM-TOKEN": "7DAE82FA2ADB4750AB347BD957867560"}
        body = json.loads(role_data[5])
        output = HttpRequest.post(url=role_data[2], headers=headers, body=body)
        expect = json.loads(role_data[6])
        actual = json.loads(output["preview"])
        assert expect == actual


def role_post():
    url = 'http://plm.hqygou.com:8088/sys/role/add'
    body = {
        "name": "设计师",
        "code": ""
    }
    headers = {
        "Content-Type": "application/json",
        "PLM-TOKEN": "7DAE82FA2ADB4750AB347BD957867560"}
    output = HttpRequest.post(url=url, headers=headers, body=body)
    print(u"请求地址：", output["request"])
    print(u"请求参数：", output["body"])
    print(u"请求结果：", output["response"])


if __name__ == '__main__':
    # role_post()
    # unittest.main(verbosity=2)
    pytest.main(["-s", "test_temp.py"])
