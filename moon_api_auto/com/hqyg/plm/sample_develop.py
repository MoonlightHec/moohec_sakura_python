# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/6 13:45 
# @Author : mhec 
# @File : sample_develop.py
# @desc : 新增样品开发数据
"""
import json
import random

from moon_api_auto.pytest_util.http_utils import HttpRequest
from moon_util.cursor_util import db


def save_sample(status=0, method='submit', token='BD34957AD50041FEB5C11ABCE855DB3C'):
    """
    新增样品开发数据
    :param token:
    :param method:
    :param status:
    :return:
    """
    # 上传图片
    img_url = 'http://plm.hqygou.com:8088/sample/develop/image/upload'
    sample_url = 'http://plm.hqygou.com:8088/sample/develop/draft/' + method
    headers = {
        'PLM-TOKEN': token,
    }
    img_name = '{}.jpg'.format(str(random.randint(1, 51)))
    img = {
        'name': img_name,
        'path': 'C:/Users/Administrator/Desktop/PLM图片/',
        'type': 'image/jpeg'}
    res = HttpRequest.file(url=img_url, headers=headers, img=img)
    if not res.get('response')['success']:
        print("token过期")
        return
    img_id = res.get('response')['data']['id']
    print('images:%s' % img_id)

    # 提交样品开发
    headers.update({'Content-Type': 'application/json'})
    # 请求json放在save_sample中
    with open('./resource/save_sample', 'r', encoding='utf8') as stream:
        data = json.load(stream)
        data['productName'] = '太阳裙0506'
        data['imageEditOutVos'][0]['id'] = img_id
        data['imageEditOutVos'][0]['name'] = img_name
        data['imageEditOutVos'][0]['url'] = "http://plm.hqygou.com:8088/image/downLoad?imageId={}".format(img_id)
        data['imageIds'] = img_id
    res = HttpRequest.post(url=sample_url, headers=headers, body=data)
    print(res.get('response'))
    if type == 'update':
        return
    if res.get('response')['success']:
        update_status(status=status, images=img_id)


def update_status(status=0, sample_code=None, images=0):
    """
    修改样品开发状态
    :param status: 样品状态
    :param sample_code: 样品编码
    :param images: 图片id
    :return:
    """
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
    save_sample(status=1, token='ED833F98C70047A981D10F10EB066C61')
    # update_status(status=1, sample_code='Y2113003328')
