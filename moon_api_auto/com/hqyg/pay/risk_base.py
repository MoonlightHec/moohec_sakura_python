# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/24 16:01 
# @Author : mhec 
# @File : risk_base.py
# @desc :
"""
# 链接数据库
from moon_util.cursor_util import db


def get_data(pay_sn=None):
    connect = db.get_connect('PAY')
    cursor = connect.cursor()
    switcher = (
        'pay_info_detail_',
        'pay_after_info_detail_',
        'pay_risk_event_'
    )
    for table_name in switcher:
        old_sql = "SELECT id,unique_id,pay_sn,order_sn FROM %s WHERE pay_sn = '%s';"
        cursor.execute(old_sql % table_name, pay_sn)
        for index in range(0, 64):
            table_num = table_name + str(index)
            sql = "SELECT id,unique_id,pay_sn,order_sn FROM %s WHERE pay_sn = '%s';"
            cursor.execute(sql % (table_num, pay_sn))
            if cursor.rowcount:
                for row in cursor.fetchall():
                    if row:
                        print("result： id:%s  unique_id:%s  pay_sn:%s  order_sn:%s\t" % row)
                print("所在表：%s" % table_num)
                print('共查找出', cursor.rowcount, '条数据\n')
    cursor.close()
    connect.close()


get_data(pay_sn='P2105250132871018390BF')
