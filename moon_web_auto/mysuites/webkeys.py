# _*_ coding: utf-8 _*_
"""
# @Time : 2020/12/15 17:00 
# @Author : River 
# @File : webkeys.py
# @desc :
"""
from selenium import webdriver


class WebKey:
    def __init__(self):
        """
        构造函数,创建必要的实例变量
        """
        self.driver = None

    def open_browser(self, br='gc'):
        """
        打开浏览器
        :param br: gc=谷歌浏览器;ff=火狐浏览器;ie=IE浏览器
        :return:
        """
        if br == 'gc':
            self.driver = webdriver.Chrome()
        elif br == 'ff':
            self.driver = webdriver.Firefox()
        elif br == 'ie':
            self.driver = webdriver.Ie()
        else:
            print("浏览器暂不支持")

    def geturl(self, url=None):
        """
        打开网站
        :param url:网站url
        :return:
        """
        self.driver.get(url)

    def click(self, locator=None):
        """
        找到并点击元素
        :param locator: 定位器，默认xPath
        :return:
        """
        self.driver.find_element_by_xpath(locator).click()

    def input(self, locator=None, value=None):
        """
        找到元素并完成输入
        :param locator: 定位器，默认xPath
        :param value: 要输入的值
        :return:
        """
        self.driver.find_element_by_xpath(locator).send_keys(value)

    def into_iframe(self, locator=None):
        """
        切换iframe
        :param locator: 定位器，默认xPath
        :return:
        """
        ele = self.driver.find_element_by_xpath(locator)
        self.driver.switch_to.frame(ele)

    def quit(self):
        """
        关闭浏览器
        :return:
        """
        self.driver.quit()
