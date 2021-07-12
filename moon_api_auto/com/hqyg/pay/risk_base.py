# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/24 16:01 
# @Author : mhec 
# @File : risk_base.py
# @desc : 风控分表查数据
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
        # 查旧表数据
        old_sql = "SELECT id,pay_sn,order_sn FROM %s WHERE pay_sn = '%s';"
        cursor.execute(old_sql % (table_name[:-1], pay_sn))
        if cursor.rowcount:
            print("\n旧表%s数据:" % table_name[:-1])
            for row in cursor.fetchall():
                print("result： id:%s  pay_sn:%s  order_sn:%s\t" % row)

        # 查新表数据
        for index in range(0, 64):
            table_num = table_name + str(index)
            sql = "SELECT id,unique_id,pay_sn,order_sn FROM %s WHERE pay_sn = '%s';"
            cursor.execute(sql % (table_num, pay_sn))
            if cursor.rowcount:
                print("新表%s数据:" % table_num)
                for row in cursor.fetchall():
                    if row:
                        print("result： id:%s  unique_id:%s  pay_sn:%s  order_sn:%s\t" % row)
                print('共查找出', cursor.rowcount, '条数据\n')
    cursor.close()
    connect.close()


if __name__ == '__main__':
    get_data(pay_sn='P2105250132871018390BF')
