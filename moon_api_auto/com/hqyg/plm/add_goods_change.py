# _*_ coding: utf-8 _*_
"""
# @Time : 2021/6/8 9:22 
# @Author : lijun7 
# @File : add_goods_change.py
# @desc : 竞品延改申请
"""
import random

from moon_api_auto.pytest_util.http_utils import HttpRequest


def submit_goods_change(token):
    # 上传图片
    img_url = 'http://plm.hqygou.com:8088/sample/color/change/audit/image/upload'
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

    # 提交竞品延改申请
    change_url = 'http://plm.hqygou.com:8088/sample/color/change/audit/add'
    headers.update({'Content-Type': 'application/json'})
    data = {
        "productName": "Braided oversize vest{}".format(str(random.randint(1, 9999))),
        "productCode": "c0p102726066",
        "goodsUrl": "https://www.bershka.com/us/braided-oversize-vest-c0p102726066.html?colorId=712",
        "cateLabel": "Sweaters and cardigans",
        "id": "",
        "imageId": img_id,
        "ownerSite": "bershka",
        "recommendFrom":3
    }
    res = HttpRequest.post(url=change_url, headers=headers, body=data)
    print(res.get('response'))


if __name__ == '__main__':
    submit_goods_change(token='8C538AE9E1A94B8A9E85DC43DB9D22B4')
