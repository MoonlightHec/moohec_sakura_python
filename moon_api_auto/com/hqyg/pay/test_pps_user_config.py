# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/7 16:45 
# @Author : mhec 
# @File : pps_user_config.py
# @desc : 用户配置中心
"""
import json

import pytest

from moon_api_auto.com.hqyg.pay.resource.pay_params import user_config_datas
from moon_api_auto.pytest_util.http_utils import HttpRequest
from moon_util.sort_yaml import ordered_yaml_load


class AssertFun:
    def __init__(self, res, assert_data):
        self.res = res
        self.assert_data = assert_data

    def assert_select(self):
        res_body = json.loads(self.res.get('response')['body'])
        config_key = res_body['data']['configKey']
        result = self.assert_data['config_key']
        print('actual:【{}】----expect:【{}】\n'.format(config_key, result))

    def assert_delete(self):
        pass

    def assert_add(self):
        pass

    def assert_update(self):
        pass


@pytest.mark.parametrize('case_datas', user_config_datas['select_cases'])
def test_user_config(case_datas):
    """
    用户配置
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    # 获取测试用例yaml文件数据
    header = {
        "service": "com.globalegrow.spi.mpay.inter.PayUserConfigService",
        "method": case_datas['method'],
        "domain": "",
        "version": "1.0.0",
        "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
    }
    body = {
        "header": header,
        "body": case_datas['body']
    }
    # 获取接口请求结果
    res = HttpRequest.post(url=url, headers=headers, body=body)

    assert_fun = AssertFun(res, case_datas['assert'])
    function = getattr(assert_fun, case_datas['assert_method'])
    function()


def user_config(method):
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    datas = ordered_yaml_load(r'./resource/pps_user_config_cases')
    case_datas = datas[method]
    for case_data in case_datas:
        # 获取测试用例yaml文件数据
        header = {
            "service": "com.globalegrow.spi.mpay.inter.PayUserConfigService",
            "method": case_data['method'],
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        }
        body = {
            "header": header,
            "body": case_data['body']
        }
        print(u'请求参数\n{}'.format(json.dumps(body, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)))
        # 获取接口请求结果
        res = HttpRequest.post(url=url, headers=headers, body=body)
        assert_fun = AssertFun(res, case_data['assert'])

        switcher = {
            'assert_delete': assert_fun.assert_delete,
            'assert_add': assert_fun.assert_add,
            'assert_update': assert_fun.assert_update,
            'select_cases': assert_fun.assert_select
        }
        # 执行断言方法
        switcher.get(method)()


if __name__ == '__main__':
    # pytest.main(['-s', 'test_pps_user_config.py'])
    user_config('select_cases')
