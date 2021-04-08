# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/25 11:56 
# @Author : mhec 
# @File : api_demo.py
# @desc : 基于flask的web service实例代码
"""

from flask import Flask, make_response, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "Emily": "hello",
    "mhec": "hi",
    "sun": "bye"
}


@auth.get_password
def get_pwd(username):
    if username in users:
        return users.get(username)
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


datas = [
    {
        "id": "25121",
        "userNo": "614614",
        "username": "lijun7",
        "name": "李军7",
        "email": "lijun7@globalegrow.com",
        "departmentId": "43441",
        "phone": "",
        "isLock": 0,
        "userEnglishName": "",
        "roleName": "商品中心-管理员",
        "departmentName": "后端研发组",
        "plmDepartmentName": None
    }
]


# 运行后请求地址：http://localhost:5000/local_api
@app.route('/local_api', methods=['POST'])
@auth.login_required
def show_datas():
    return jsonify({'datas': datas})


if __name__ == '__main__':
    app.run(debug=True)
