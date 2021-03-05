# _*_ coding: utf-8 _*_
"""
# @Time : 2020/11/26 11:04 
# @Author : River 
# @File : runner.py
# @desc :
"""
import os

import pytest

pytest.main(['-s', './ddt/commerce_test.py', '--alluredir', './temp'])
# pytest.main(['-s', './test_example4.py', '--alluredir', './temp'])
# 用例失败时重新跑2次
# pytest.main(['-s', './ddt/commerce_test.py', '--reruns', '2'])
os.system('allure generate ./temp -o ./report --clean')
