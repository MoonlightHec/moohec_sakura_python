# _*_ coding: utf-8 _*_
"""
# @Time : 2021/1/26 16:59 
# @Author : River 
# @File : order_base.py
# @desc : 查询订单信息
"""

# 链接数据库
from moon_util.cursor_util import db

cursor = db.get_cursor('PPS')
# 查询订单信息(order_sn,paySn)
data = ('U2103162119443049', '')
sql_par = {}
print(
    "id    parent_trade_sn        trade_sn               parent_order_sn      pay_sn                   site_code  pay_status \t")
# 获取sql查询语句及where条件
if data[0]:
    sql_par[0] = 'parent_order_sn'
    sql_par[1] = data[0]
else:
    sql_par[0] = 'pay_sn'
    sql_par[1] = data[1]
for index in range(1, 64):
    table_num = 'pay_gateway_' + str(index)
    sql = "SELECT id,parent_trade_sn,trade_sn,parent_order_sn,pay_sn,site_code,pay_status FROM %s WHERE %s = '%s';"
    cursor.execute(sql % (table_num, sql_par[0], sql_par[1]))
    if cursor.rowcount:
        for row in cursor.fetchall():
            print("%s %s %s %s %s      %s      %s\t" % row)
        print("支付状态pay_status(0-未支付 1-处理中 2-已支付 3-退款中 4-退款成功 5退款失败 6支付失败)")
        print("所在库：%s" % table_num)
        print('共查找出', cursor.rowcount, '条数据')
