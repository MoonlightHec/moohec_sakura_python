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


def get_oms_webmin_headers():
    """
    获取带cookies的headers
    :return:
    """
    url = 'https://10.60.34.197:8100/session_login.cgi'
    headers = {
        "Cookie": "testing=1; sid=x"
    }
    data = {
        "page": "/",
        "user": "oms",
        "pass": "aTb8R3Rm2G9",
        "save": 1
    }

    # 获取cookies
    res = requests.post(url=url, headers=headers, data=data, verify=False, allow_redirects=False)
    cookiejar = res.cookies
    sid = requests.utils.dict_from_cookiejar(cookiejar)['sid']
    headers['Cookie'] = 'testing=1; sid={}'.format(sid)
    return headers


class WebminObj:
    def __init__(self, script_name):
        self.headers = get_oms_webmin_headers()
        self.headers['Referer'] = 'https://10.60.34.197:8100/cron/edit_cron.cgi'
        self.save_url = 'https://10.60.34.197:8100/cron/save_cron.cgi'
        # 获取脚本通用参数
        with open('./resource/webmin_script_data.json', 'r', encoding='utf-8') as data_stream:
            self.data = json.load(data_stream)
        # 获取要执行的脚本参数
        with open('./resource/webmin_args.json', 'r', encoding='utf8') as params_stream:
            self.params = json.load(params_stream)[script_name]
        self.execute_url = 'https://10.60.34.197:8100/cron/exec_cron.cgi?idx={}'

    def run_script(self, *args):
        # 获取要执行的脚本参数
        self.data['idx'] = 1191
        self.data['comment'] = self.params['comment']
        self.data['cmd'] = self.params['cmd'].format(*args)
        # 禁止重定向，否则重定向到/cron/exec_cron.cgi后，执行会因为没有cookie导致执行脚本报权限不足
        print("\n----------------------------开始保存脚本----------------------------")
        save_res = requests.get(url=self.save_url, headers=self.headers, params=self.data, verify=False, allow_redirects=False)
        if save_res.status_code == 302:
            print("\n----------------------------保存成功----------------------------")

        # 执行脚本
        print("\n----------------------------开始执行脚本----------------------------")
        exec_res = requests.get(url=self.execute_url.format(1191), headers=self.headers, verify=False)
        print(exec_res.text)
        with open('./resource/webmin_script_result.html', 'w', encoding='utf-8') as fd:
            fd.write(exec_res.text)


if __name__ == '__main__':
    web_script = WebminObj('match_payment_info')
    web_script.run_script('20092400941522369351')
