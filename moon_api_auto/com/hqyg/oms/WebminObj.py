# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/26 17:24 
# @Author : lijun7 
# @File : WebminObj.py
# @desc :
"""
import requests
from flask import json

# 禁用安全警告信息；requests忽略ssl证书后，控制台不再输出警告信息
requests.packages.urllib3.disable_warnings()


def get_headers(url, data):
    """
    获取headers
    :param url:
    :param data:
    :return:
    """
    headers = {
        "Cookie": "testing=1; sid=x"
    }
    # 获取cookies
    res = requests.post(url=url, headers=headers, data=data, verify=False, allow_redirects=False)
    cookiejar = res.cookies
    sid = requests.utils.dict_from_cookiejar(cookiejar)['sid']
    headers['Cookie'] = 'testing=1; sid={}'.format(sid)
    return headers


def get_oms_webmin_headers():
    """
    获取oms带cookies的headers
    :return:
    """
    url = 'https://10.60.34.197:8100/session_login.cgi'
    data = {
        "page": "/",
        "user": "oms",
        "pass": "aTb8R3Rm2G9",
        "save": 1
    }
    return get_headers(url, data)


def get_sms_webmin_headers():
    """
    获取sms带cookies的headers
    :return:
    """
    url = 'https://10.60.48.185:8100/session_login.cgi'
    data = {
        "page": "/",
        "user": "www",
        "pass": "9z4BXFjt3A4Kcg==",
    }
    return get_headers(url, data)


class WebminObj:
    def __init__(self, app_name='oms', script_name=None):
        switcher = {
            'oms': get_oms_webmin_headers,
            'sms': get_sms_webmin_headers,
        }
        app_name = app_name.lower()
        self.headers = switcher.get(app_name)()

        # 获取脚本通用参数
        with open('./resource/webmin_script_data.json', 'r', encoding='utf-8') as data_stream:
            self.data = json.load(data_stream)
        # 获取要执行的脚本参数
        with open('./resource/webmin_args.json', 'r', encoding='utf8') as params_stream:
            request_info = json.load(params_stream)[app_name]
            self.params = request_info[script_name]
            self.headers['Referer'] = request_info['config']['Referer']
            self.data['idx'] = request_info['config']['idx']
            self.data['user'] = request_info['config']['user']
            self.save_url = request_info['config']['save_url']
            self.execute_url = request_info['config']['execute_url'].format(self.data['idx'])

    def run_script(self, *args):
        # 获取要执行的脚本参数
        self.data['comment'] = self.params['comment']
        self.data['cmd'] = self.params['cmd'].format(*args)
        # 禁止重定向，否则重定向到/cron/exec_cron.cgi后，执行会因为没有cookie导致执行脚本报权限不足
        print("\n----------------------------开始保存脚本----------------------------")
        save_res = requests.get(url=self.save_url, headers=self.headers, params=self.data, verify=False, allow_redirects=False)
        if save_res.status_code == 302:
            print("\n----------------------------保存成功----------------------------")
            # 执行脚本
            print("\n----------------------------开始执行脚本----------------------------")
            exec_res = requests.get(url=self.execute_url, headers=self.headers, verify=False)
            print(exec_res.text)
            with open('./resource/webmin_script_result.html', 'w', encoding='utf-8') as fd:
                fd.write(exec_res.text)
        else:
            print("\n----------------------------脚本保存失败----------------------------")


if __name__ == '__main__':
    """
    # 同步soa订单
    # 地址异常生成电联工单
    # 推送异常工单到wos
    # 退款到原支付 param：【826:WAX_CC】
    # 退款到电子钱包 param：退款申请编号
    # 推送邮件队列列表到SMS param：【ticket_receive】
    # 自动去信加入队列
    """
    web_script = WebminObj(app_name='oms', script_name='soa_order_into_mq')
    try:
        web_script.run_script('U2109292222525828','22')
    except IndexError:
        print("参数个数错误")
