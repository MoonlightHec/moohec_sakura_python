# _*_ coding: utf-8 _*_
"""
# @Time : 2021/2/4 14:38 
# @Author : River 
# @File : add_color.py
# @desc : 造待加色数据
"""
import json
import time

from moon_api_auto.pytest_util.HttpUtils import HttpRequest


def color_add_select():
    """
    添加加色款
    :return:
    """
    sku = "206119401"
    headers = {
        "Content-Type": "application/json",
        "PLM-TOKEN": "466BEB68A062433FB7FAA881E0C6178D"}

    # 查询sku信息
    url_select = 'http://plm.hqygou.com:8088/reproofing/product/one/add'
    data_select = {"sku": sku}
    output_select = HttpRequest.post(url=url_select, headers=headers, body=data_select)
    if output_select.get('response')['code'] == 900000005:
        print(output_select.get('response'))
    elif output_select.get('response')['code'] == 0:
        color = output_select.get('response')['data']['color']
        color_id = output_select.get('response')['data']['colorId']
        goodsSn = output_select.get('response')['data']['sku']
        productCode = output_select.get('response')['data']['productCode']
        product_img = output_select.get('response')['data']['productImg']
        size_id = output_select.get('response')['data']['sizeId']
        size = output_select.get('response')['data']['size']

        # 添加加色款
        url_add = 'http://plm.hqygou.com:8088/sample/develop/color/change/add'
        data_add = {
            "inVoList": [
                {"id": "",
                 "bizCode": 1,
                 "color": color,
                 "colorId": color_id,
                 "goodsSn": goodsSn,
                 "productCode": productCode,
                 "productImg": product_img,
                 "productLabel": "4",
                 "recommendFrom": 1,
                 "errorMsg": "",
                 "sizeId": size_id,
                 "size": size,
                 "sku": goodsSn,
                 "purchasePrice": "",
                 "reproofingRemark": "",
                 "reproofingLabel": "",
                 "reproofingSn": "",
                 "dataFrom": "",
                 "purchaseUser": "",
                 "purchaseUserName": "",
                 "purchaseName": "",
                 "remark": ""}]}
        output = HttpRequest.post(url=url_add, headers=headers, body=data_add)
        print("添加加色request:%s\nbody：\n%s\nresponse:\n%s" % (
            output.get('request'), json.dumps(data_add, indent=4, ensure_ascii=False), output.get('preview')))
    else:
        print("未知错误 TODO")


def pdm_receive_edit():
    """
    pdm收样，编辑确认
    :return:
    """
    sample_goods_sn = 'Y2113003195'
    PHPSESSID = 'gdidd5berd6kb4r284aqlbmf60'
    purchase_id = None

    url_purchase = 'http://pdm.hqygou.com/sample/sample-develop/index?act=getReceiveEditList'
    url_receive = 'http://pdm.hqygou.com/sample/sample-develop/index?act=editReceiveSample'
    url_edit = 'http://pdm.hqygou.com/sample/sample-develop/index?act=editResure'
    cookie = {
        # "_ga": "GA1.2.1161475107.1602492055",
        # "Hm_lvt_90859506e7af61dd6690c7a11180810b": "1602492056",
        # "Hm_lvt_f1d9b7402cd80f0b26458d932e1698be": "1608021211,1610417660",
        "PHPSESSID": PHPSESSID
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # 获取purchase_id
    data_purchase = {'page': '1', 'pageSize': '5', 'sample_goods_sn': sample_goods_sn, 'act': 'getReceiveEditList'}
    output_purchase = HttpRequest.post(url=url_purchase, headers=headers, cookies=cookie, body=data_purchase)
    if output_purchase.get('preview'):
        purchase_id = output_purchase.get('response')['data']['lists'][0]['id']
        print("purchase_id:%s" % purchase_id)
    else:
        print("cookie过期response:\n%s\n" % output_purchase.get('response').text)

    # 编辑收样
    data_receive = {'purchase_id': purchase_id, 'remark': '5'}
    output_receive = HttpRequest.post(url=url_receive, headers=headers, cookies=cookie, body=data_receive)
    print("编辑收样request:%s\nresponse:\n%s\n" % (output_receive.get('request'), output_receive.get('preview')))

    # 编辑确认
    time.sleep(2)
    data_edit = {
        'edit_reject_reason': '',
        'remark': '',
        'sample_goods_sn': sample_goods_sn,
        'purchase_id': purchase_id,
        'type': '1',
        'is_batch': '0',
        'repeat_sku': ''}
    output_edit = HttpRequest.post(url=url_edit, headers=headers, cookies=cookie, body=data_edit)
    print("编辑确认request:%s\nresponse:\n%s" % (output_edit.get('request'), output_edit.get('preview')))


if __name__ == '__main__':
    color_add_select()
    # pdm_receive_edit()
