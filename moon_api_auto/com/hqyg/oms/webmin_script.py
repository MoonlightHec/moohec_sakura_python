# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/23 17:58 
# @Author : lijun7 
# @File : webmin_script.py
# @desc :
"""
import requests


def push_to_wos():
    """
    同步oms审批单到wos
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
    headers['Referer'] = 'https://10.60.34.197:8100/cron/edit_cron.cgi?idx=674'

    # 开始执行脚本
    exec_res = requests.get(url='https://10.60.34.197:8100/cron/exec_cron.cgi?idx=674', headers=headers, verify=False)
    print(exec_res.text)


if __name__ == '__main__':
    push_to_wos()
