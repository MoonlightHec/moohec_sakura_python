# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/19 16:37 
# @Author : River 
# @File : init_department_apm.py
# @desc : 初始化组织架构apmPlus(待加色列表所有用到的apm)
"""
from moon_util.cursor_util import db


class initApm:
    def __init__(self, my_cursor, role_id):
        self.cursor = my_cursor
        self.role_id = role_id

    def delete_apm(self):
        """
        删除原始组织架构设计师数据
        :param role_id:
        :return:
        """
        delete_sql = 'DELETE FROM t_plm_department_user_rel WHERE department_id = %s'
        self.cursor.execute(delete_sql, self.role_id)
        connect.commit()
        print(self.cursor.rowcount, "record(s) deleted")

    def select_apm(self):
        """
        组装设计师名字数据
        :return:
        """
        select_sql = 'SELECT id,username,name FROM t_sys_user WHERE id IN(SELECT designer FROM t_sample_color_change_info GROUP BY designer);'
        self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        value_list = []
        for user in result:
            name_str = user[2] + '(' + user[1] + ')'
            depart_user = (self.role_id, user[0], name_str)
            value_list.append(depart_user)
        return tuple(value_list)

    def insert_apm(self):
        """
        插入新设计师名字数据
        :return:
        """
        insert_sql = 'INSERT INTO t_plm_department_user_rel(department_id,user_id,`name`,is_delete,create_user,update_user) VALUEs(%s,%s,%s,1,25121,25121);'
        apm_info = self.select_apm()
        self.cursor.executemany(insert_sql, apm_info)
        connect.commit()
        print(self.cursor.rowcount, "record(s) inserted")


if __name__ == '__main__':
    connect = db.get_cursor('PLM')
    cursor = connect.cursor()
    initApm = initApm(cursor, 4)

    initApm.delete_apm()
    initApm.insert_apm()

    cursor.close()
    connect.close()
