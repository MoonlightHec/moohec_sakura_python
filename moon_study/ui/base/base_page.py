# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/24 9:41 
# @Author : mhec
# @File : base_page.py
# @desc :
"""

from selenium.common.exceptions import NoSuchElementException


class WebDriver:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *loc):
        """单个定位元素的方法"""
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException as e:
            print('Error Details {0}'.format(e.args[0]))

    def find_elements(self, *loc):
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException as e:
            print('Error Details {0}'.format(e.args[0]))
