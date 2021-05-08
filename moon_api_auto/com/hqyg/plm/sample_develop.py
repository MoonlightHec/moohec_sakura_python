# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/6 13:45 
# @Author : mhec 
# @File : sample_develop.py
# @desc : 新增样品开发数据
"""
import json
import logging
import random

from moon_api_auto.pytest_util.http_utils import HttpRequest
from moon_util.cursor_util import db

logging.basicConfig(format='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def save_sample(status=0):
    # 上传图片
    img_url = 'http://plm.hqygou.com:8088/sample/develop/image/upload'
    img_headers = {
        'PLM-TOKEN': '41F0DEF90252484D88CEEBDDD190E9BD',
    }
    img_name = '{}.jpg'.format(str(random.randint(1, 51)))
    img = {
        'name': img_name,
        'path': 'C:/Users/Administrator/Desktop/PLM图片/',
        'type': 'image/jpeg'}
    res = HttpRequest.file(url=img_url, headers=img_headers, img=img)
    img_id = res.get('response')['data']['id']

    # 保存样品开发
    save_url = 'http://plm.hqygou.com:8088/sample/develop/draft/submit'
    save_headers = {
        'PLM-TOKEN': '41F0DEF90252484D88CEEBDDD190E9BD',
        'Content-Type': 'application/json'
    }

    # 请求json放在save_sample中
    with open('./resource/save_sample', 'r', encoding='utf8') as stream:
        data = json.load(stream)
        data['productName'] = '太阳裙0506'
        data['imageEditOutVos'][0]['id'] = img_id
        data['imageEditOutVos'][0]['name'] = img_name
        data['imageEditOutVos'][0]['url'] = "http://plm.hqygou.com:8088/image/downLoad?imageId={}".format(img_id)
        data['imageIds'] = img_id
    res = HttpRequest.post(url=save_url, headers=save_headers, body=data)
    logging.info(res.get('response'))
    print(res.get('response'))
    if res == 200 and status:
        update_status(status=status, images=img_id)


def update_status(status=0, sample_code=0, images=0):
    connect = db.get_connect('PLM')
    cursor = connect.cursor()
    param = 0
    if sample_code:
        param = sample_code
        sql = "UPDATE t_sample_develop_info SET `status`=%s WHERE sample_code=\'%s\';"
    elif images:
        param = images
        sql = "UPDATE t_sample_develop_info SET `status`=%s WHERE images=%s;"
    cursor.execute(sql % (status, param))
    connect.commit()
    print(u'状态修改数据条数：%s' % str(cursor.rowcount))


if __name__ == '__main__':
    # save_sample(status=2)
    update_status(status=1, sample_code='Y2113003303')

